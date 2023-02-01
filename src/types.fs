module NativeBuilder.Types

type Author = {
    name : string;
    email : string;
}

type Project = {
    name : string;
    dependencies: string System.Collections.Generic.List option;
    author : Author option;
    version : string option;
    always_mingw : bool option;
    ``type``: string option;
    cpp_standard: string option;
}
