from typing import Any, Dict, List, Iterable
import ast
import copy
import types
import typing

from .types import PathLike

TYPES_BLACKLIST = [types.FunctionType, types.ModuleType]  # TODO other things like classes
AST_IMPORT = [ast.Import, ast.ImportFrom]
AST_LOOP = [ast.For, ast.While]


def exclude_value(key: str, value: Any, pre_provided: Iterable[str]):
    if key in pre_provided:  # if it's part of the variables provided to the configuration
        return True
    if key.startswith("__"):  # TODO consider if this is really needed
        return True
    if key in typing.__all__:  # type: ignore
        # TODO only for python 3.5
        return True
    if type(value) in TYPES_BLACKLIST:
        return True
    return False


def filter_values(dictionary: Dict[str, Any], pre_provided: Iterable[str]) -> dict:
    return {
        key: value
        for key, value in dictionary.items()
        if not exclude_value(key, value, pre_provided)
    }
