from __future__ import annotations
import subprocess
import sys
import shlex
import json
import os
import platform

from native_build.config import Config, CONFIG_PATH, ROOT

class CMake:

    @classmethod
    def sync(cls):
        proj = Config.read()

