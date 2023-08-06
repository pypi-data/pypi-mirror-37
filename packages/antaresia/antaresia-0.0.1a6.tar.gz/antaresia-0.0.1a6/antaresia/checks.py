from typing import List, Union
import ast
import os
import shutil
import sys

import mypy.api

from .exceptions import ForbiddenImport, MyPyFail
from .types import PathLike

__all__ = ["check_mypy"]


def check_ast_nodes(node: ast.Module, filename: PathLike, allowed_imports: List[str]):
    """
    Checks if ast doesn't have disalowed constructs
    """
    for sub_node in ast.walk(node):
        if isinstance(sub_node, ast.ImportFrom):
            module_name = sub_node.module
            if module_name not in allowed_imports:
                raise ForbiddenImport(filename, sub_node.lineno, module_name)
        elif isinstance(sub_node, ast.Import):
            # mypy doesn't recognize that sub_node can only be Import or ImportFrom
            for module in  sub_node.names:
                module_name = module.name  # type: ignore
                if module_name not in allowed_imports:
                    raise ForbiddenImport(filename, sub_node.lineno, module_name)
        elif isinstance(sub_node, ast.Attribute):
            attribute = sub_node.attr
            if attribute.startswith("__"):
                # TODO Test
                # TODO proper Exception
                raise Exception(
                    f"{filename}:{sub_node.lineno}: error: "
                    f"Accessing private attribute {attribute} is forbidden."
                )


def check_mypy(filename: PathLike):
    stdout, stderr, exit_code = mypy.api.run([os.fsdecode(filename)])
    if exit_code != 0:
        print(stdout, file=sys.stderr)
        if stderr:
            print(stderr, file=sys.stderr)
        raise MyPyFail()
