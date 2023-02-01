from native_builder.project import *
from pathlib import Path


print(
    parse_project("""
    {
        "name": "a"
    }
    """)
)

from native_builder.project import *
from pathlib import Path

a = parse_project("""
    {
        "name": "a"
    }
""")

print(
    unparse_project(a)
)

