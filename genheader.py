from pprint import pformat
import pkgutil
import pathlib
import wisepy2
import shutil

# links = ['fable_library']
# for package in pkgutil.walk_packages(__import__('fable_library').__path__):
#     links.append(f'fable_library.{package.name}')
# source_code = f"""# This file is generated by genheader.py
# from __future__ import annotations
# import sys
# from importlib import import_module

# link_modules = {pformat(links)}

# for source in link_modules:
#     module = import_module(source)
#     target = ".".join([__name__, source])
#     sys.modules[target] = module
#     del source
#     del target
#     del module
# """

source_code = ""

def run(package: str):
    pathlib.Path(f'{package}/fable_modules/__init__.py').write_text(source_code, encoding='utf-8')
    shutil.copytree(f'fable_library', f'{package}/fable_modules/fable_library')

wisepy2.wise(run)()
