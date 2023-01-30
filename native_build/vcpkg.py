from __future__ import annotations
import subprocess
import sys
import shlex
import json
import os
import platform

from native_build.config import Config, CONFIG_PATH, ROOT
from native_build.project import Project
from colorama import Fore, Back, Style

def check64bit():
    return sys.maxsize > 2**32

class VCPkg:
    @staticmethod
    def init_config():
        if CONFIG_PATH.exists():
            return
        CONFIG_PATH.write_text(
            json.dumps(Project(name = ROOT.name), indent=4, ensure_ascii=False),
            encoding="utf-8"
        )
        print(Fore.GREEN + "init native-build.json success!" + Style.RESET_ALL)

    @staticmethod
    def vcpkg_root():
        return ROOT.joinpath("GitDependencies", "microsoft", "vcpkg")

    @classmethod
    def call_vcpkg_bootstrap(cls):
        if cls.vcpkg_root().joinpath("vcpkg.exe").exists():
            return
        if cls.vcpkg_root().joinpath("vcpkg").exists():
            return
        try:
            if os.name == 'nt':
                suffix = "bat"
            else:
                suffix = "sh"

            subprocess.check_call(
                [
                    cls.vcpkg_root().joinpath(f"bootstrap-vcpkg.{suffix}")
                ]
            )
            VCPkg.call_vcpkg('integrate', 'install')
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"bootstrapping vcpkg failed!" + Style.RESET_ALL)
            sys.exit(1)

    @classmethod
    def call_vcpkg(cls, *args: str):
        try:
            env = os.environ.copy()
            env['VCPKG_DEFAULT_TRIPLET'] = cls.default_triplet()
            env['VCPKG_DEFAULT_HOST_TRIPLET'] = cls.default_triplet()

            subprocess.check_call(
                [
                    cls.vcpkg_root().joinpath("vcpkg").as_posix(),
                    *args
                ],
                env=env
            )
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"call vcpkg ({shlex.join(args)}) failed!" + Style.RESET_ALL)
            sys.exit(1)

    @staticmethod
    def default_triplet():
        if sys.platform.startswith("win32"):
            if check64bit():
                if Config.read().get("always_mingw"):
                    return "x64-mingw-dynamic"
                else:
                    return "x64-windows-dynamic"
            else:
                if Config.read().get("always_mingw"):
                    return "x86-mingw-dynamic"
                else:
                    return "x86-windows-dynamic"
        elif sys.platform.startswith("linux"):
            if check64bit():
                return "x64-linux"
            else:
                return "x86-linux"
        elif sys.platform.startswith("darwin"):
            if check64bit():
                return "x64-osx"
            else:
                return "x86-osx"
        else:
            raise NotImplementedError(f"unknown platform {sys.platform}")

    @classmethod
    def CMAKE_TOOLCHAIN_FILE(cls):
        return cls.vcpkg_root().joinpath('scripts', 'buildsystems', 'vcpkg.cmake')
