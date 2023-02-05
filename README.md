# NativeBuilder

NativeBuilder is an easy-to-use and cross-platform tool for building native applications leveraging the power of VCPkg and CMake.

Currently, NativeBuilder is internal only and not ready for production use. It is made public for reproducing native binaries referenced in our Julia+C/C++ projects and creating templates for technical tests.

## Usage

```shell
nb init          # init project
nb install yoga  # install dependencies
nb remove raylib # remove dependencies
nb build --main  # create the executable under build/
nb build         # create the library under build/
```

Note that NativeBuilder is still in development, and is not responsible for dependency management.

## Troubleshooting

1. When changing `always_mingw`, later build might get failed. This is due to your IDE (such as VSCode with C/CPP extensions) is using `vcpkg/buildtrees` which prevents NativeBuilder from rebuilding the dependencies. To fix this, you might close your IDE, call `nb build` again and reopen your C/C++ IDE.


2. To support C/C++ intellisense in VSCode, install CMake Tools, and create a `c_cpp_properties.json` in the `.vscode` directory:

    ```json
    {
        "configurations": [
            {
                "compileCommands": "${workspaceFolder}/build/compile_commands.json",
                "configurationProvider": "ms-vscode.cmake-tools"
            }
        ],
        "version": 4
    }
    ```