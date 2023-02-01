from setuptools import setup, find_packages
from datetime import datetime
from pathlib import Path


version = 0.1
with Path('README.md').open() as readme:
    readme = readme.read()


setup(
    name='native_builder',
    version=version if isinstance(version, str) else str(version),
    keywords="", # keywords of your project that separated by comma ","
    description="", # a concise introduction of your project
    long_description=readme,
    long_description_content_type="text/markdown",
    license='mit',
    python_requires='>=3.6.0',
    url='https://github.com/Suzhou-Tongyuan/Native-Builder',
    author='Suzhou-Tongyuan',
    author_email='support@tongyuan.cc',
    packages=find_packages(),
    entry_points={"console_scripts": [
        'nb=native_builder.cmd:main'
    ]},
    install_requires=[
        'aiohttp',
        'colorama',
        'dulwich',
        'loguru',
    ], # dependencies
    platforms="any",
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
    ],
    zip_safe=False,
)


