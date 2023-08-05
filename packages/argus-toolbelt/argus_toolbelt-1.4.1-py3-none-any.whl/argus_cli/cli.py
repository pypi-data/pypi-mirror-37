from colorama import init, deinit
from pprint import pprint

from api_generator import load
from argus_cli.settings import settings, update_settings  # Settings has to be before the logger!
from argus_cli.helpers.log import log
from argus_cli.arguments import get_command_arguments, get_plugin_arguments, register_command_metadata, get_command, \
    get_program_arguments
from argus_cli.plugin import run_command, load_plugin_module, get_plugin_modules


def setup() -> None:
    """Reads program arguments, sets up the API and loads plugins"""
    arguments = get_program_arguments()
    if arguments.get("apikey"):
        update_settings(["api", "api_key"], arguments["apikey"])

    load(settings["api"]["api_url"], settings["api"]["definitions"])

    plugins = get_plugin_modules(settings["cli"]["plugins"])
    log.info("Loading plugins...")
    for plug in plugins:
        load_plugin_module(plug)


def run() -> None:
    """Parses command and runs the application"""
    plugin_name, command_name = get_plugin_arguments()
    register_command_metadata(plugin_name, command_name)

    arguments = get_command_arguments()

    # TODO: Should be more configurable
    # Remove program-wide arguments because they'll fuck with run_command (they're not in the actual function)
    del arguments["debug"]
    del arguments["apikey"]

    func = get_command(plugin_name, command_name).function
    log.debug("Running command \"%s %s\"" % (plugin_name, command_name))
    result = run_command(func, arguments)

    if result:
        pprint(result)


def main() -> None:
    """Used to launch the application"""
    # Initialize colorama to enable Windows color support
    init()

    # Initialize and run argus cli
    setup()
    run()

    # Deinitialize colorama
    deinit()
