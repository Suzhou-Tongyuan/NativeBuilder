from __future__ import annotations
from .ajson import (obj_from_json, parse_json, serialize_json, obj_to_json)
from .types import (Project_reflection, Project)

def parse_project(str_1: str) -> Project:
    return obj_from_json(Project_reflection(), parse_json(str_1))


def unparse_project(project: Project) -> str:
    return serialize_json(obj_to_json(Project_reflection(), project))


__all__ = ["parse_project", "unparse_project"]

