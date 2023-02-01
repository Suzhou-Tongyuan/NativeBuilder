# NativeBuilder

NativeBuilder is an easy-to-use tool for building native applications.

## Usage

```
nb init          # init project
nb install yoga  # install dependencies
nb remove raylib # remove dependencies
nb build         # create executable under build/
```

Note that NativeBuilder is still in development, and is not responsible for dependency management.

## Troubleshooting

1. When changing `always_mingw`, later build might get failed. This is due to your IDE (such as VSCode with C/CPP extensions) is using `vcpkg/buildtrees` which prevents NativeBuilder from rebuilding the dependencies. To fix this, you might close your IDE, call `nb build` again and reopen your C/C++ IDE.
