module NativeBuilder.API
open AJson

open NativeBuilder.Types

let parse_project (str: string) = deserialize<Project>(str)
let unparse_project (project: Project) = serialize(project)