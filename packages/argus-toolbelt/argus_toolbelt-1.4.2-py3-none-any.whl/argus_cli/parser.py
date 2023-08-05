import collections
import inspect
import re
from pydoc import locate

from argus_cli.helpers.formatting import to_caterpillar_case
from argus_cli.helpers.log import log


def parse_function(function: callable) -> dict:
    """Parses a functions parameters and help-text from its docstring and annotations.

    :param function: A function
    :return: The description and arguments (in order) for the function
    """
    parsed = {}

    log.debug("Parsing arguments and docstring for %s..." % function.__name__)

    parsed["arguments"] = _parse_parameters(function)

    if function.__doc__:
        parsed = _parse_docstring(function, parsed)

    return parsed


def _parse_parameter(name: str, parameter: inspect.Parameter) -> dict:
    """Parses a parameter"""
    log.debug("Parsing parameter %s" % name)

    argument = {
        "names": [_get_parameter_name(name, parameter)],
        "dest": name if _is_required(parameter) is False else None,
        "required": _is_required(parameter),
        "nargs": _get_number_of_arguments(parameter),
        "action": _get_action(parameter),
        "choices": _get_choices(parameter),
        "type": _get_type(parameter),
        "default": _get_default(parameter),
    }

    # Some of the arguments are not allowed for all actions (eg. nargs in argparse._StoreFalseAction).
    # Thus we have to remove the ones that are None to not have argparse crash.
    argument = {k: v for k, v in argument.items() if v is not None}

    if not _is_valid_argument(parameter, argument):
        raise ValueError("Parameter %s is not valid" % name)
    return argument


def _parse_parameters(function: callable) -> dict:
    """Parses a functions parameters.

    :param function: The function to parse
    :returns: All arguments, ready to pass to argparse
    """
    arguments = collections.OrderedDict()
    signature = inspect.signature(function)

    log.debug("%s arguments: %s" % (function.__name__, signature))

    for name, parameter in signature.parameters.items():
        if parameter.kind == inspect.Parameter.VAR_KEYWORD:
            # **kwargs Have to be defined in docstrings
            log.debug("**%s argument ignored. kwargs are added from the docstring." % name)
            continue
        arguments[name] = _parse_parameter(name, parameter)

    log.debug("%s: Registered commands from signature:\n\t%s" % (function.__name__, arguments))
    return arguments


def _parse_docstring_parameters(docstring: str, arguments: dict) -> dict:
    """Parses the docstring for extra info about parameters.

    :param docstring: The docstring to parse
    :param arguments: Existing arguments
    """
    #: Gets doc for a parameter. `argument_type` is optional.
    param_regex = re.compile(r":param\s?(?P<argument_type>\w*) (?P<name>\w+): (?P<doc>.*)")

    for argument_type, name, doc in param_regex.findall(docstring):
        argument = arguments.setdefault(
            name,
            {"names": [to_caterpillar_case(name)], "dest": name, "required": False}
        )

        _type = locate(argument_type) if argument_type else None
        if inspect.isclass(_type) and issubclass(_type, (list, tuple)):
            argument["nargs"] = "*"
        elif _type:
            if argument.get("action"):
                # If there is an action, it means we have a boolean. Ignore.
                # NOTE: If _get_action()'s behavior changes, this might cause side-effects
                continue
            if argument.get("type"):
                log.warning(
                    "Argument %s is set in both function annotation and docstring. Prioritizing docstring." % name
                )
            argument["type"] = _type

        # This has to go after the block above as the type might change.
        argument["help"] = doc

        if argument.get("type") is str:
            argument["help"] += \
                "\n Use @ prefix on file paths to read a file into the argument, e.g @/path/to/file.txt"

    return arguments


def _parse_docstring_aliases(docstring: str, arguments: dict) -> dict:
    """Parses the docstring for parameter aliases

    :param docstring: The docstring to parse
    :param arguments: Existing arguments
    """
    #: Gets aliases for a parameter
    alias_regex = re.compile(r":alias (?P<name>\w+):\s+(?P<aliases>.*)")

    for name, aliases in alias_regex.findall(docstring):
        if name not in arguments:
            raise NameError("%s is not an argument. An argument has to exist to be aliased." % name)
        for alias in aliases.split(","):
            arguments[name]["names"].append(to_caterpillar_case(alias.strip()))

    return arguments


def _parse_docstring(function: callable, parsed: dict) -> dict:
    """Parses a function's docstring for more info about it and it's parameters.

    :param function: The function to parse
    :param parsed: Existing arguments for the function
    :return: Short description, Long description and more argument info
    """
    # Escape all % { and } so argparse doesnt crash when trying to format the string
    docstring = function.__doc__.replace("{", "{{").replace("}", "}}").replace("%", "%%").split("\n", 1)

    parsed["help"] = docstring[0].strip()

    if len(docstring) <= 1:
        return parsed

    description = docstring[1]

    match = re.compile(r":(?:param|alias)").search(description)
    arguments_part = description[match.start():] if match else None
    parsed["description"] = (description[:match.start()] if match else description).strip()

    if arguments_part:
        parsed["arguments"] = _parse_docstring_parameters(arguments_part, parsed["arguments"])
        parsed["arguments"] = _parse_docstring_aliases(arguments_part, parsed["arguments"])

    return parsed


def _is_required(parameter: inspect.Parameter) -> bool:
    """Weather or not the parameter is required"""
    # If the parameter has no default value it's either a positional, vararg or kwarg.
    # positionals, varargs and kwargs are not allowed to have ""
    if parameter.kind is inspect.Parameter.VAR_POSITIONAL:
        return None
    elif parameter.default is not parameter.empty:
        return False
    return None


def _get_number_of_arguments(parameter: inspect.Parameter) -> str:
    """Gets the number of arguments to be accepted for the parameter"""
    if inspect.isclass(parameter.annotation) and issubclass(parameter.annotation, (list, tuple)) \
            or parameter.kind == inspect.Parameter.VAR_POSITIONAL:
        return "*"
    else:
        return None


def _get_action(parameter: inspect.Parameter) -> str:
    """Gets a parameter's action (if any)"""
    if not isinstance(parameter.annotation, bool) and parameter.annotation is not bool:
        return None
    if parameter.default is inspect.Parameter.empty:
        return None
    elif not parameter.default:
        return "store_true"
    else:
        return "store_false"


def _get_choices(parameter: inspect.Parameter) -> list:
    """Gets a sequence of choices (if any)"""
    if not isinstance(parameter.annotation, collections.Container) or isinstance(parameter.annotation, str):
        return None
    elif any(
            isinstance(element, collections.Container) and not isinstance(element, str)
            for element in parameter.annotation
    ):
        raise ValueError("A list of choices can not have a nested iterable object.")

    return parameter.annotation


def _get_type(parameter: inspect.Parameter) -> collections.Callable:
    """Returns a type if it's a callable"""
    if inspect.isclass(parameter.annotation) and issubclass(parameter.annotation, (list, tuple)):
        # list() and tuple() should be parsed as nargs, not a type.
        return None
    if isinstance(parameter.annotation, collections.Sequence):
        # If it is a sequence it will be nargs
        return None
    elif (isinstance(parameter.annotation, bool) or parameter.annotation is bool) \
            and parameter.default is not inspect.Parameter.empty:
        # Bools are defined by the "action" option
        return None
    elif not callable(parameter.annotation):
        # The type has to be callable
        return None
    return parameter.annotation if parameter.annotation is not inspect.Parameter.empty else None


def _get_default(parameter: inspect.Parameter):
    """Gets a parameter's default if applicable"""
    if parameter.default is parameter.empty:
        return None
    return parameter.default


def _is_valid_argument(parameter: inspect.Parameter, argument: dict) -> bool:
    """Checks weather or not an argument is valid

    To verify that a argument is valid, we have to check that:
        * It has no annotation (meaning that there is nothing to parse)
        * It has a type, action, choice or nargs (which are mutaly exlusive)
    """
    return parameter.annotation is parameter.empty \
           or argument.get("type") \
           or argument.get("action") \
           or argument.get("choices") \
           or argument.get("nargs")


def _get_parameter_name(name: str, parameter: inspect.Parameter):
    """Gets the name of a parameter

    The given name can be changed if it has a default value == true.
    This is done to reflect that the flag will negate the value.
    """
    name = to_caterpillar_case(name)

    if parameter.default is True:
        return "no-%s" % name if len(name) > 1 else name
    return name


