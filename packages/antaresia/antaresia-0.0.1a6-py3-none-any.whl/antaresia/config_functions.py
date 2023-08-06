"""
Functions available inside the configuration files
"""
from typing import Any
import inspect
import os
import urllib.parse

from .loaders import load
from .types import PathLike

__all__ = ["include_config", "read"]


def __relative_to_cwd(file_path: PathLike) -> str:
    """
    Gets the path to ``file_path`` relative to the current working dir so it can be read
    """
    frame = inspect.currentframe()
    assert frame is not None
    try:
        # We have to go back to levels, the function that called this function and the configuration
        # file that called that function
        calling_function_frame = frame.f_back
        if calling_function_frame is not None:
            calling_config_frame = calling_function_frame.f_back
        else:
            # TODO proper user friendly error
            raise Exception("Couldn't load config scope.")
        parent_filename = calling_config_frame.f_code.co_filename
        assert parent_filename is not None
    finally:
        del frame
    path = urllib.parse.urljoin(parent_filename, os.fsdecode(file_path))
    return path


def include_config(relative_path: PathLike):
    """
    Imports configuration from ``relative_path`` and appends it to the caller locals
    """
    # TODO: detect circles?
    path = __relative_to_cwd(relative_path)

    frame = inspect.currentframe()
    assert frame is not None
    try:
        importer_locals = frame.f_back.f_locals
    finally:
        del frame

    imported_configuration = load(path)
    importer_locals.update(imported_configuration)


def read(file_path: PathLike) -> str:
    """
    Read the content of ``file_path`` and return it as a string.
    """
    path = __relative_to_cwd(file_path)
    with open(path, "r") as file_object:
        content = file_object.read()
    return content
