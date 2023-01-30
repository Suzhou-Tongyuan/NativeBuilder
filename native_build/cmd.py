import sys
from wisepy2 import wise
from native_build.config import CONFIG_PATH, Config
from native_build.project import Project
from native_build.git import git_dep
from native_build.vcpkg import VCPkg
from colorama import Fore, Style

class Cmd:
    @staticmethod
    def init(vcpkg_url: str = r"https://github.com/microsoft/vcpkg"):
        VCPkg.init_config()
        print(Fore.GREEN + "creating vcpkg cache..." + Style.RESET_ALL)

        git_dep("microsoft/vcpkg", vcpkg_url)

        VCPkg.call_vcpkg_bootstrap()

        print(Fore.GREEN + "project init success!" + Style.RESET_ALL)

    @staticmethod
    def install(package_name: str):
        proj = Config.read()
        deps = proj.get("dependencies", [])
        if package_name not in deps:
            deps.append(package_name)
            VCPkg.call_vcpkg("install", package_name)
        proj["dependencies"] = deps
        Config.write()
        print(Fore.GREEN + f"install {package_name} success!")

    @staticmethod
    def remove(package_name: str):
        proj = Config.read()
        deps = proj.get("dependencies", [])
        if package_name in deps:
            VCPkg.call_vcpkg("remove", package_name)
            deps.remove(package_name)
        proj["dependencies"] = deps
        Config.write()
        print(Fore.GREEN + f"remove {package_name} success!")

def main():
    wise(Cmd)()
