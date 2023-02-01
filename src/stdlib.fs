module Python.Stdlib
open System
open Fable.Core

[<Import("Path", "pathlib")>]
type Path(path: string) =
    [<Emit("$0.absolute()")>]
    member _.absolute(): Path = nativeOnly

    [<Emit("$0.joinpath($1...)")>]
    member _.joinpath([<ParamArray>] sections: string []): Path = nativeOnly

