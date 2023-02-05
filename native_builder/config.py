from __future__ import annotations
import subprocess
from pathlib import Path
from colorama import Fore, Back, Style
from native_builder.project import Project, parse_project, unparse_project
import sys
import json
import typing
import shlex
import os

def _find_root(p: Path):
    for each in p.iterdir():
        if each.name == "native-build.json":
            return p

    if p.parent == p:
        return Path.cwd()

    return _find_root(p.parent)

ROOT = _find_root(Path.cwd())

CONFIG_PATH = ROOT.joinpath("native-build.json")

class Config:
    CONFIG_DATA: Project | None = None
    use_main: bool = False


    @classmethod
    def read(cls):
        data = cls.CONFIG_DATA
        if data is not None:
            return typing.cast(Project, data)
        try:
            data = parse_project(CONFIG_PATH.read_text(encoding="utf-8"))
        except Exception as e:
            print(Fore.RED + str(e) + Style.RESET_ALL)
            sys.exit(1)
        cls.CONFIG_DATA = data
        return data

    @classmethod
    def write(cls):
        if cls.CONFIG_DATA is None:
            return
        CONFIG_PATH.write_text(
            unparse_project(cls.CONFIG_DATA),
            encoding="utf-8"
        )
