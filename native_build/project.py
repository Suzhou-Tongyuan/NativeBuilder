from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING, cast
if TYPE_CHECKING:
    from typing_extensions import NotRequired, TypeGuard

class FalseInfo:
    def __init__(self, message: str):
        self.message = message

    def __bool__(self):
        return False

    def __repr__(self):
        return self.message

class Author(TypedDict):
    name: str
    email: NotRequired[str]


def validate_author(data) -> TypeGuard[Author]:
    if not isinstance(data, dict):
        return cast(bool, FalseInfo("author must be a dict"))
    if not isinstance(data.get("name"), str):
        return cast(bool, FalseInfo("author.name must be a str"))
    if not isinstance(data.get("email", ""), str):
        return cast(bool, FalseInfo("author.email must be a str"))
    return True

class Triplet(TypedDict):
    arch: str
    static: NotRequired[bool]

def validate_triplet(data) -> TypeGuard[Triplet]:
    if not isinstance(data, dict):
        return cast(bool, FalseInfo("triplet must be a dict"))
    if not isinstance(data.get("arch"), str):
        return cast(bool, FalseInfo("triplet.arch must be a str"))
    if not isinstance(data.get("dynamic", False), bool):
        return cast(bool, FalseInfo("triplet.dynamic must be a bool"))
    return True

class Project(TypedDict):
    name: str
    dependencies: NotRequired[list[str]]
    author: NotRequired[str | list[Author]]
    triplet: NotRequired[Triplet]
    host_triplet: NotRequired[Triplet]
    always_mingw: NotRequired[bool]

def validate_project(data) -> TypeGuard[Project]:
    if not isinstance(data, dict):
        return cast(bool, FalseInfo("project must be a dict"))
    if not isinstance(data.get("name"), str):
        return cast(bool, FalseInfo("project.name must be a str"))
    if not isinstance(data.get("dependencies", []), list):
        return cast(bool, FalseInfo("project.dependencies must be a list"))
    for each in data.get("dependencies", []):
        if not isinstance(each, str):
            return cast(bool, FalseInfo(f"project.dependencies must be a list of str, got an entry {each}"))
    if not isinstance(data.get("author", []), list):
        return cast(bool, FalseInfo("project.author must be a list"))
    for each in data.get("author", []):
        msg = validate_author(each)
        if not msg:
            return msg

    msg = validate_triplet(data.get("triplet", {}))
    if not msg:
        return msg
    msg = validate_triplet(data.get("host_triplet", {}))
    if not msg:
        return msg
    if not isinstance(data.get("always_mingw", False), bool):
        return cast(bool, FalseInfo("project.always_mingw must be a bool"))
    return True
