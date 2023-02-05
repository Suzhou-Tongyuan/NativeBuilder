from __future__ import annotations
from dataclasses import dataclass
from typing import Optional
from .fable_modules.fable_library.reflection import (TypeInfo, string_type, record_type, array_type, option_type, bool_type)
from .fable_modules.fable_library.types import (Record, Array)

def _expr0() -> TypeInfo:
    return record_type("NativeBuilder.Types.Author", [], Author, lambda: [("name", string_type), ("email", string_type)])


@dataclass(eq = False, repr = False)
class Author(Record):
    name: str
    email: str

Author_reflection = _expr0

def _expr1() -> TypeInfo:
    return record_type("NativeBuilder.Types.Project", [], Project, lambda: [("name", string_type), ("dependencies", option_type(array_type(string_type))), ("author", option_type(Author_reflection())), ("version", option_type(string_type)), ("always_mingw", option_type(bool_type)), ("main", option_type(string_type)), ("library", option_type(string_type)), ("include", option_type(array_type(string_type))), ("cpp_standard", option_type(string_type))])


@dataclass(eq = False, repr = False)
class Project(Record):
    name: str
    dependencies: Optional[Array[str]]
    author: Optional[Author]
    version: Optional[str]
    always_mingw: Optional[bool]
    main: Optional[str]
    library: Optional[str]
    include: Optional[Array[str]]
    cpp_standard: Optional[str]

Project_reflection = _expr1

__all__ = ["Author_reflection", "Project_reflection"]

