from __future__ import annotations
import shutil
import io
import sys
import os
from pathlib import Path
from native_builder.config import Config, ROOT
from native_builder.vcpkg import VCPkg
from subprocess import check_call, CalledProcessError
from colorama import Fore, Back, Style

def drop_suffix(x: str, suffixes: list[str]):
    for suffix in suffixes:
        if x.endswith(suffix):
            return x[:-len(suffix)]
    return x

def drop_prefix(x: str, prefixes: list[str]):
    for prefix in prefixes:
        if x.startswith(prefix):
            return x[len(prefix):]
    return x

def _extract_library_name(x: str):
    x = drop_suffix(x, [".dll.lib", ".lib", ".dll.a", ".a"])
    x = drop_prefix(x, ["lib"])
    return x

def _is_library(x: str):
    return x.endswith(".lib") or x.endswith(".a")

def get_all_libraries(lib_directory: Path):
    if lib_directory.exists() and lib_directory.is_dir():
        for each in lib_directory.iterdir():
            if each.is_file() and _is_library(each.name):
                yield _extract_library_name(each.name)

class CMake:

    @classmethod
    def call_cmake(cls, *args: str):
        try:
            if os.name == 'nt':
                cmd = "cmake.exe"
            else:
                cmd = "cmake"

            check_call(
                [
                    cmd,
                    *args
                ]
            )
        except CalledProcessError as e:
            print(Fore.RED + f"cmake failed:\n{e}" + Style.RESET_ALL)
            sys.exit(1)

    @classmethod
    def sync(cls):
        buf = io.StringIO()
        proj = Config.read()

        print("cmake_minimum_required(VERSION 3.21)", file=buf)
        print("project({} VERSION {})".format(proj.name, proj.version or "0.0.1"), file=buf)
        print("set(CMAKE_BUILD_TYPE Release)", file=buf)

        print(file=buf)

        print("# https://cmake.org/cmake/help/latest/module/GenerateExportHeader.html", file=buf)
        print("set(CMAKE_CXX_VISIBILITY_PRESET hidden)", file=buf)
        print("set(CMAKE_VISIBILITY_INLINES_HIDDEN 1)", file=buf)
        print("set(CMAKE_EXPORT_COMPILE_COMMANDS 1)", file=buf)

        print(file=buf)

        print("set (CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})", file=buf)
        print("set (CMAKE_LIBRARY_OUTPUT_DIRECTORY_RELEASE \"${CMAKE_LIBRARY_OUTPUT_DIRECTORY}\")", file=buf)
        print("set (CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR})", file=buf)
        print("set (CMAKE_RUNTIME_OUTPUT_DIRECTORY_RELEASE \"${CMAKE_RUNTIME_OUTPUT_DIRECTORY}\")", file=buf)

        print(file=buf)

        print("set(CMAKE_C_STANDARD 99)", file=buf)
        print("set(CMAKE_CXX_STANDARD {})".format(proj.cpp_standard or "14"), file=buf)

        print(file=buf)

        target_directory = VCPkg.vcpkg_root().joinpath("installed", VCPkg.get_target_triplet())
        print("include_directories({})".format(target_directory.joinpath("include").absolute().as_posix()), file=buf)
        print("link_directories({})".format(target_directory.joinpath("lib").absolute().as_posix()), file=buf)

        print(file=buf)

        print("include_directories(${CMAKE_SOURCE_DIR}/include)", file=buf)
        print("include_directories(${CMAKE_CURRENT_BINARY_DIR})", file=buf)

        print(file=buf)

        proj.type = proj.type or "executable"
        if proj.type == "library":
            print("add_library(${PROJECT_NAME} SHARED src/library.cpp)", file=buf)
            print("include(GenerateExportHeader)", file=buf)
            print("GENERATE_EXPORT_HEADER(${PROJECT_NAME}", file=buf)
            print("  EXPORT_FILE_NAME {}_export.h".format(proj.name.lower()), file=buf)
            print("  EXPORT_MACRO_NAME {}_EXPORT".format(proj.name.upper()), file=buf)
            print(")", file=buf)
        elif proj.type == "executable":
            print("    add_executable(${PROJECT_NAME} src/main.cpp)", file=buf)
        else:
            print(Fore.RED + "Invalid project type: '{}', expect 'executable' or 'library'".format(proj.type) + Style.RESET_ALL)
            sys.exit(1)

        for lib in get_all_libraries(target_directory.joinpath("lib")):
            print("target_link_libraries(${PROJECT_NAME} %s)" % lib, file=buf)

        print(file=buf)

        print("if (WIN32)", file=buf)
        print("    message(\"Win32: linking windows libraries\")", file=buf)
        print("    target_link_libraries(${PROJECT_NAME} ntdll)", file=buf)
        print("    target_link_libraries(${PROJECT_NAME} msvcrt)", file=buf)
        print("    target_link_libraries(${PROJECT_NAME} kernel32)", file=buf)
        print("    target_link_libraries(${PROJECT_NAME} user32)", file=buf)
        print("    target_link_libraries(${PROJECT_NAME} winmm)", file=buf)
        print("endif()", file=buf)

        print("# Checks if OSX and links appropriate frameworks (only required on MacOS)", file=buf)
        print("if (APPLE)", file=buf)
        print("    target_link_libraries(${PROJECT_NAME} \"-framework IOKit\")", file=buf)
        print("    target_link_libraries(${PROJECT_NAME} \"-framework Cocoa\")", file=buf)
        print("    target_link_libraries(${PROJECT_NAME} \"-framework OpenGL\")", file=buf)
        print("endif()", file=buf)

        with open(ROOT.joinpath("CMakeLists.txt"), "w") as f:
            f.write(buf.getvalue())

    @classmethod
    def copy_binary(cls):
        bin = VCPkg.binary_directory()
        if bin.exists() and bin.is_dir():
            for each in bin.iterdir():
                if each.is_dir():
                    shutil.copytree(bin, ROOT.joinpath("build"))
                else:
                    shutil.copy(each, ROOT.joinpath("build"))

