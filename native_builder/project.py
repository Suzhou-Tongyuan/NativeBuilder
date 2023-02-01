from __future__ import annotations
from safe_config.types import Project
from safe_config.api import parse_project, unparse_project as _unparse_project
import json

__all__ = [
    "parse_project",
    "unparse_project",
    "Project",
]

def unparse_project(project: Project) -> str:
    d = json.loads(_unparse_project(project))
    for key in list(d):
        if d[key] is None:
            del d[key]

    return json.dumps(d, ensure_ascii=False, indent=4)
