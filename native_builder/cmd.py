import sys
import os
from wisepy2 import wise
from native_builder.config import CONFIG_PATH, ROOT, Config
from native_builder.git import git_dep
from native_builder.vcpkg import VCPkg
from native_builder.cmake import CMake
from colorama import Fore, Style

class Cmd:
    @staticmethod
    def init(vcpkg_url: str = r"https://github.com/microsoft/vcpkg"):
        VCPkg.init_config()
        print(Fore.GREEN + "creating vcpkg cache..." + Style.RESET_ALL)

        git_dep("microsoft/vcpkg", vcpkg_url)

        VCPkg.call_vcpkg_bootstrap()
        CMake.sync()
        print(Fore.GREEN + "project init success!" + Style.RESET_ALL)

    @staticmethod
    def install(package_name: str):
        proj = Config.read()
        deps = proj.dependencies or []
        if package_name not in deps:
            deps.append(package_name)
        VCPkg.call_vcpkg("install", package_name + ':' + VCPkg.get_target_triplet())
        proj.dependencies = deps
        Config.write()
        CMake.sync()
        print(Fore.GREEN + f"install {package_name} success!")

    @staticmethod
    def remove(package_name: str, fullArch: bool = False):
        proj = Config.read()
        deps = proj.dependencies or []
        if package_name in deps:
            deps.remove(package_name)

        VCPkg.call_vcpkg("remove", package_name + ':' + VCPkg.get_target_triplet())
        proj.dependencies = deps
        Config.write()
        CMake.sync()
        print(Fore.GREEN + f"remove {package_name} success!")

    @staticmethod
    def clean():
        build_dir = ROOT.joinpath("build")
        print(Fore.BLUE + "cleaning cmake build directory..." + Style.RESET_ALL)
        if build_dir.exists():
            import shutil
            shutil.rmtree(build_dir)
        print(Fore.BLUE + "cleaning vcpkg buildtrees directory..." + Style.RESET_ALL)
        VCPkg.clean_cache()
        print(Fore.GREEN + "clean success!" + Style.RESET_ALL)

    @staticmethod
    def build(noCache: bool = False):
        if noCache:
            Cmd.clean()

        for each in Config.read().dependencies or []:
            Cmd.install(each)

        CMake.sync()
        build_dir = ROOT.joinpath("build")
        build_dir.mkdir(exist_ok=True, parents=True, mode=0o777)
        os.chdir(build_dir)
        if "windows" in VCPkg.get_host_triplet():
            # TODO: support earlier version of visual studio
            generator = "Visual Studio 17 2022"
        else:
            generator = "Unix Makefiles"
        CMake.call_cmake('-G', generator, "..")
        CMake.call_cmake("--build", ".", '--config', 'Release')
        CMake.copy_binary()

def main():
    wise(Cmd)()
