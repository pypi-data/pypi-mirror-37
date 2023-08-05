import sys

import argparse
from argparse import ArgumentParser
from collections import namedtuple

from argus_cli.parser import parse_function
from argus_cli.helpers.collections import ImmutableDeepDict
from argus_cli.helpers.log import log

#: The key of the plugin argument
_PLUGIN_ARGUMENT = "_plugins"
# Storage location for the parsers
_PLUGIN_PARSER = "_parser"
_PLUGIN_SUBPARSER = "_subparser"

_Command = namedtuple("Command", ("parser", "function"))


class PluginParserContainer(object):
    """A container that handles plugin parsers

    Each node in the dict has three objects.
        _subparsers: The _SubParserAction object (that you add parsers to)
        _parser: The actual parser. This is just used for testing
        Everything else: Commands and sub-plugins
    """
    class _StorePlugin(argparse._SubParsersAction):
        """Makes plugin subparsers store the used subparser in one list."""
        def __call__(self, parser, namespace, values, option_string=None):
            super().__call__(parser, namespace, values, option_string)

            # Values will be all arguments after this plugin.
            # Just get the name of this plugin.
            values = values[0]
            if not hasattr(namespace, _PLUGIN_ARGUMENT):
                setattr(namespace, _PLUGIN_ARGUMENT, [values])
            else:
                getattr(namespace, _PLUGIN_ARGUMENT).insert(0, values)

    def __init__(self, main_parser):
        self._dict = ImmutableDeepDict()
        self._plugin_parser = main_parser.add_subparsers(
            action=self._StorePlugin,
            help="Which plugin to use",
        )

    def __str__(self):
        return str(self._dict)

    def _command_exists(self, plugin: dict, command: str, func: callable):
        """Checks if a function already exists.

        It will also check the function's __code__ as they might be the same function.
        This can occur if a function is registered twice, ie. via an module import.
        """
        return command in plugin and func.__code__ != plugin[command].function.__code__

    def _add_parser(self, path: tuple) -> ArgumentParser:
        """Adds a plugin's parser to the tree."""
        plugin_name = path[-1]
        if len(path) == 1:
            # This is a top level plugin
            parent_parser = self._plugin_parser
        else:
            try:
                parent_parser = self._dict[path[:-1]][_PLUGIN_SUBPARSER]
            except KeyError:
                # A key-error means that the parent doesn't have a parser.
                parent_parser = self._add_parser(path[:-1])

        new_parser = parent_parser.add_parser(plugin_name, parents=[_BASE_PARSER])
        new_subparser = new_parser.add_subparsers(action=self._StorePlugin)
        self._dict[path] = {
            _PLUGIN_PARSER: new_parser,  # Used for testing
            _PLUGIN_SUBPARSER: new_subparser
        }

        return new_subparser

    def add_parser(self, path: tuple) -> None:
        """Adds a parser to the container"""
        self._add_parser(path)

    def add_command(self, plugin_name: tuple, command_name: str, func: callable) -> ArgumentParser:
        """Adds a command to a plugin parser"""
        plugin = self._dict[plugin_name]
        plugin_parser = plugin[_PLUGIN_SUBPARSER]

        if self._command_exists(plugin, command_name, func):
            raise NameError(
                "Command '%s' already registered by %s. Cannot re-assign to %s"
                % (command_name, plugin[command_name].function.__code__.co_filename, func.__code__.co_filename)
            )

        plugin[command_name] = _Command(
            plugin_parser.add_parser(command_name, parents=[_BASE_PARSER]),
            func
        )

        return plugin[command_name].parser

    def get_plugin(self, plugin: tuple):
        """Gets a plugin parser"""
        return self._dict[plugin]

    def get_command(self, plugin: tuple, command_name: str):
        """Gets a command from a plugin"""
        return self._dict[plugin][command_name]


#: This parser contains all the base arguments of
_BASE_PARSER = ArgumentParser(add_help=False)
_BASE_PARSER.add_argument(
    "--debug",
    action="store_true",
    help="Adds debug logging to the program"
)
_BASE_PARSER.add_argument(
    "--apikey",
    help="Manually define the argus-api key"
)

#: The parser to rule them all!
_ROOT_PARSER = ArgumentParser(fromfile_prefix_chars='@', parents=[_BASE_PARSER])
#: Parsers that handles a plugins commands
_PARSERS = PluginParserContainer(_ROOT_PARSER)


def register_command(plugin_sequence: tuple, command_name: str, func: callable) -> None:
    """Registers a command towards a plugin.

    :param plugin_sequence: The name of the plugin that the function belongs to
    :param command_name: The name of the function
    """
    log.debug("Registering command \"%s\" in plugin \"%s\"" % (command_name, "/".join(plugin_sequence)))
    try:
        _PARSERS.add_command(plugin_sequence, command_name, func)
    except KeyError:
        log.debug("The given plugin sequence did not exist, creating.")
        _PARSERS.add_parser(plugin_sequence)
        _PARSERS.add_command(plugin_sequence, command_name, func)


def register_command_metadata(plugin_sequence: tuple, command_name: str) -> None:
    """Registers the function metadata to a parser

    Registering the metadata is done at a later point to not do unnecessary operations with _parse_function().
    A single call to _parse_function() takes quite some time, so it's better to do it JIT.

    :param plugin_sequence: The name of the plugin
    :param command_name: The name of the command
    :param function: The function to parse metadata from
    """
    log.debug("Registering metadata for \"%s\" on plugin \"%s\"" % (command_name, "/".join(plugin_sequence)))

    command = _PARSERS.get_command(plugin_sequence, command_name)
    metadata = parse_function(command.function)
    parser = command.parser

    parser.help = metadata.get("help")
    parser.description = metadata.get("description")

    for argument, options in metadata["arguments"].items():
        names = options.pop("names")

        if options.get("required") is False:
            prefixed_names = []
            for name in names:
                prefix = "-" if len(name) is 1 else "--"
                prefixed_names.append(prefix + name)
            names = prefixed_names
        elif len(names) > 1:
            log.warn("%s is a positional argument, and can thus not have an alias. Ignoring aliases." % names[0])
            names = [names[0]]

        parser.add_argument(*names, **options)


def get_command(plugin: tuple, command: str) -> _Command:
    return _PARSERS.get_command(plugin, command)


def get_program_arguments() -> dict:
    """Parse arguments that concern the program itself"""
    log.debug("Parsing program arguments")

    arguments = vars(_BASE_PARSER.parse_known_args()[0])

    return arguments


def get_plugin_arguments() -> tuple:
    """Only parse the plugin arguments.

    Plugin arguments are the <plugin> and <command> part of the CLI.
    If we do not do it like this help-messages for commands would be catched in here,
    and thus we wouldn't get a proper help message for commands.

    :returns: Plugin and command name
    """
    def error_or_help(parser):
        if any(keyword in sys.argv for keyword in ("--help", "-h")):
            parser.print_help()
            parser.exit()
        parser.error("Not enough arguments")

    log.debug("Parsing plugin arguments")

    base_args = [arg for arg in sys.argv[1:] if arg != "--help"]
    args = vars(_ROOT_PARSER.parse_known_args(base_args)[0])

    if _PLUGIN_ARGUMENT not in args:
        error_or_help(_ROOT_PARSER)

    plugin_name = tuple(args[_PLUGIN_ARGUMENT][:-1])
    command_name = args[_PLUGIN_ARGUMENT][-1]

    try:
        parser = _PARSERS.get_command(plugin_name, command_name)
    except KeyError:
        parser = _PARSERS.get_plugin(command_name)  # If there is just one argument it will end up here

    if not isinstance(parser, _Command):
        error_or_help(parser[_PLUGIN_PARSER])

    return plugin_name, command_name


def get_command_arguments() -> dict:
    """Gets the command arguments.

    See get_plugin_arguments() for why we do it like this.

    :returns: Command arguments
    """
    log.debug("Parsing command arguments")

    parsed = vars(_ROOT_PARSER.parse_args())
    # Remove plugin arguments as they aren't necessary for the command arguments
    parsed.pop(_PLUGIN_ARGUMENT)

    return parsed
