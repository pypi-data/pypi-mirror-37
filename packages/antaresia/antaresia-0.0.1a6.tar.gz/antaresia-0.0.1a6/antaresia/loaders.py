from typing import Optional, List
import ast
import functools
import multiprocessing
import typing

from .checks import check_ast_nodes, check_mypy
from .exceptions import Timeout
from .filters import filter_values
from .types import PathLike, Seconds

EXPRESSION_SEPARATOR = "### antaresia return:"


def _real_load_string(
    return_dict: dict,
    code: str,
    filename: PathLike = ".",
    variables: Optional[dict] = None,
    allowed_imports: Optional[List[str]] = None,
):
    """
    Function that actually generates the configuration.

    ``return_dict`` is a dictionary that is shared with the parent process and should contain
    a ``value`` key if the configuration is generated and ``exception`` key if an exception occurs.
    """
    try:
        allowed_imports = allowed_imports if allowed_imports is not None else ["typing"]

        if filename != ".":  # if we have a real filename
            check_mypy(filename)

        expression: Optional[str]
        if EXPRESSION_SEPARATOR in code:
            code, expression = code.split(EXPRESSION_SEPARATOR)
        else:
            expression = None

        root_node: ast.Module = ast.parse(code)
        check_ast_nodes(root_node, filename=filename, allowed_imports=allowed_imports)

        config_globals = {}
        pre_provided = set()
        # TODO do this only in python 3.6 (annotations are not evaluated by default on 3.7)
        for var in typing.__all__:  # type: ignore
            config_globals[var] = getattr(typing, var)
            pre_provided.add(var)
        if variables:  # add user provided variables
            config_globals.update(variables)
            pre_provided.update(variables.keys())

        compiled_code = compile(root_node, filename, "exec")
        exec(compiled_code, config_globals)
        values = filter_values(config_globals, pre_provided=pre_provided)
        if expression is not None:
            configuration = eval(expression, {}, values)
        else:
            configuration = values
    except Exception as exception:
        return_dict["exception"] = exception
    else:
        return_dict["value"] = configuration


def load_string(
    code: str,
    filename: PathLike = ".",
    variables: Optional[dict] = None,
    allowed_imports: Optional[List[str]] = None,
    timeout: Optional[Seconds] = None,
):
    """
    Loads a configuration from a ``code`` string.
    
    ``variables`` are passed to configuration code.

    All imports are disallowed if not included in ``allowed_imports``.

    If ``timeout`` is set and the configuration takes more than ``timeout`` seconds to be processed
    an Exception is raised.
    """
    manager = multiprocessing.Manager()
    return_dict: dict = manager.dict()
    loading_process = multiprocessing.Process(
        target=_real_load_string,
        args={return_dict},
        kwargs={
            "code": code,
            "filename": filename,
            "variables": variables,
            "allowed_imports": allowed_imports,
        },
    )
    loading_process.start()
    loading_process.join(timeout)
    if timeout is not None and loading_process.is_alive():
        loading_process.terminate()
        raise Timeout(filename, timeout)
    exception = return_dict.get("exception")
    if exception:
        raise exception
    return return_dict["value"]


def load(
    filename: PathLike,
    variables: Optional[dict] = None,
    allowed_imports: Optional[List[str]] = None,
    timeout: Optional[Seconds] = None,
):
    with open(filename) as configuration_file:
        configuration_source = configuration_file.read()
        return load_string(
            configuration_source,
            filename,
            variables,
            allowed_imports=allowed_imports,
            timeout=timeout,
        )
