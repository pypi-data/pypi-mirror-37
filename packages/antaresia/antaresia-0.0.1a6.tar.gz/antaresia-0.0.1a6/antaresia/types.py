"""
Useful type definitions.
"""

from typing import Union, NewType
import os 

__all__ = ['PathLike']

PathLike = Union[str, bytes, 'os.PathLike[str]']
Seconds = NewType('Seconds', float)