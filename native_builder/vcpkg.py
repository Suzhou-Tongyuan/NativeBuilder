from __future__ import annotations
import subprocess
import sys
import shlex
import json
import shutil
import os
import platform

from native_builder.config import Config, CONFIG_PATH, ROOT
from native_builder.project import Project, parse_project, unparse_project
from colorama import Fore, Back, Style
from contextlib import contextmanager

def check64bit():
    return sys.maxsize > 2**32

@contextmanager
def use_vcpkg_env():
    old_env = os.environ.copy()
    try:
        os.environ["VCPKG_ROOT"] = str(VCPkg.vcpkg_root())
        os.environ["VCPKG_DEFAULT_TRIPLET"] = VCPkg.get_target_triplet()
        yield
    finally:
        os.environ.clear()
        os.environ.update(old_env)

class VCPkg:
    @staticmethod
    def init_config():
        if CONFIG_PATH.exists():
            return

        proj = parse_project('{"name": ""}')
        proj.name = ROOT.name

        CONFIG_PATH.write_text(
            unparse_project(proj),
            encoding="utf-8"
        )
        print(Fore.GREEN + "init native-build.json success!" + Style.RESET_ALL)

    @staticmethod
    def vcpkg_root():
        return ROOT.joinpath("GitDependencies", "microsoft", "vcpkg")

    @classmethod
    def library_directory(cls):
        return cls.vcpkg_root().joinpath("installed", cls.get_target_triplet(), "lib")

    @classmethod
    def include_directory(cls):
        return cls.vcpkg_root().joinpath("installed", cls.get_target_triplet(), "include")

    @classmethod
    def binary_directory(cls):
        return cls.vcpkg_root().joinpath("installed", cls.get_target_triplet(), "bin")

    @classmethod
    def call_vcpkg_bootstrap(cls):
        if cls.vcpkg_root().joinpath("vcpkg.exe").exists():
            return
        if cls.vcpkg_root().joinpath("vcpkg").exists():
            return
        try:
            with use_vcpkg_env():
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
            with use_vcpkg_env():
                subprocess.check_call(
                    [
                        cls.vcpkg_root().joinpath("vcpkg").as_posix(),
                        *args
                    ]
                )
        except subprocess.CalledProcessError as e:
            print(Fore.RED + f"call vcpkg ({shlex.join(args)}) failed!" + Style.RESET_ALL)
            sys.exit(1)

    @classmethod
    def clean_cache(cls):
        shutil.rmtree(
            cls.vcpkg_root().joinpath("buildtrees").absolute().as_posix(),
            ignore_errors=True
        )

    @classmethod
    def get_target_triplet(cls):
        return cls.default_triplet()

    @classmethod
    def get_host_triplet(cls):
        return cls.default_triplet()

    @staticmethod
    def default_triplet():
        if sys.platform.startswith("win32"):
            if check64bit():
                if Config.read().always_mingw:
                    return "x64-mingw-dynamic"
                else:
                    return "x64-windows"
            else:
                if Config.read().always_mingw:
                    return "x86-mingw-dynamic"
                else:
                    return "x86-windows"
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
