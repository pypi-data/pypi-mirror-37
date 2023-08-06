from typing import Optional
from .types import PathLike, Seconds

class AntaresiaException(Exception): pass

class MyPyFail(AntaresiaException):
    def __str__(self):
        # TODO improve
        return "Failed MyPy Check."

class ForbiddenImport(AntaresiaException):
    def __init__(self, filename: PathLike, line_number:int, module:Optional[str]) -> None:
        self.filename=filename
        self.line_number=line_number
        self.module=module

    def __str__(self):
        return f"{self.filename}:{self.line_number}: Importing '{self.module}' is not allowed."


class Timeout(AntaresiaException):
    def __init__(self, filename: PathLike, seconds:Seconds) -> None:
        self.filename=filename
        self.seconds=seconds

    def __str__(self):
        seconds = f'1 second' if self.seconds == 1 else f'{self.seconds} seconds'
        return f"{self.filename}: Failed to load in {seconds}."