module AJson
open Microsoft.FSharp.Reflection

type Json =
        | JInt of int64
        | JFloat of double
        | JBool of bool
        | JStr of string
        | JNull
        | JList of Json ResizeArray
        | JDict of (string * Json) ResizeArray
    with
    member this.kind =
        match this with
        | JInt _ -> "int"
        | JFloat _ -> "float"
        | JBool _ -> "bool"
        | JStr _ -> "string"
        | JNull _ -> "null"
        | JList _ -> "list"
        | JDict _ -> "dict"


module Parsec =
    type Parser<'a> = int -> string -> int * 'a
    let pChar_ (c: char) =
        let apply (i: int) (s: string) =
            if i >= s.Length || s.[i] <> c then invalidOp "unexpected match"
            else (i + 1, ())
        apply

    let pStr_ (pat: string) =
        let apply (i: int) (s: string) =

            if i + pat.Length > s.Length || s.[i..i+pat.Length - 1] <> pat then invalidOp "unexpected match"
            else (i + pat.Length, ())
        apply

    let pChar (c: char) =
        let apply (i: int) (s: string) =
            if i >= s.Length || s.[i] <> c then invalidOp "unexpected match"
            else (i + 1, c)
        apply

    let pCharset_ (cs : char array) =
        let apply (i: int) (s: string) =
            if i >= s.Length then invalidOp "unexpected match"
            elif Array.contains s.[i] cs then (i+1, ())
            else invalidOp "unexpected match"
        apply

    let pCharset (cs : char array) =
        let apply (i: int) (s: string) =
            if i >= s.Length then invalidOp "unexpected match"
            elif Array.contains s.[i] cs then (i+1, s.[i])
            else invalidOp $"unexpected match {s.[i]}"
        apply

    let pIgnore (p: Parser<'a>) : Parser<unit> =
        let apply i s =
            let i, _ = p i s
            (i, ())
        apply

    let pSeq_ (ps: Parser<unit> list): Parser<unit> =
        let apply (i: int) (s: string) =
            let rec loop i ps =
                if i >= s.Length then invalidOp "unexpected match"
                else
                match ps with
                | hd::tl ->
                    let i, _ =  hd i s
                    loop i tl
                | [] -> i, ()
            loop i ps
        apply

    let pSepRep (sep: Parser<bool>) (p: Parser<'a>): Parser<'a ResizeArray> =
        let apply (i: int) (s: string) =
            let res = ResizeArray<'a>()
            let rec loop i =
                if i >= s.Length then invalidOp "unexpected match"
                else
                let i, v = p i s
                res.Add(v)
                let i, test = sep i s
                if test then loop i
                else i, res
            loop i
        apply

    let pSpc : Parser<unit> =
        let apply (i: int) (s: string) =
            let rec loop i =
                if i >= s.Length then i, ()
                else
                match s.[i] with
                | ' ' | '\n' | '\r' | '\t' -> loop (i + 1)
                | _ -> i, ()
            loop i
        apply


    let allowSPC (p: Parser<'a>): Parser<'a> =
        let apply (i: int) (s: string) =
            let i, _ = pSpc i s
            let i, v = p i s
            let i, _ = pSpc i s
            i, v
        apply

    let la1 (dispatch: char -> Parser<'a>): Parser<'a> =
        let apply (i: int) (s: string) =
            if i >= s.Length then invalidOp "unexpected match"
            let p = dispatch(s.[i])
            p i s
        apply

    let pNumber : Parser<string> =
        let apply (i: int) (s: string) =
            if i >= s.Length then invalidOp "unexpected match"
            let start = i
            let rec loop j =
                if j >= s.Length then j
                else
                match s.[j] with
                | '.' | 'E' | 'e' | '-' -> loop (j + 1)
                | c when c <= '9'  && c >= '0' -> loop (j + 1)
                | _ -> j
            let i = loop i
            i, s.[start..i-1]
        apply

    let pStr : Parser<string> =
        let apply (i: int) (s: string) =
            if i >= s.Length || s.[i] <> '"' then
                invalidOp $"incomplete parsing for string"
            let buf = System.Text.StringBuilder()
            let mutable find_end = false
            let mutable i = i + 1
            while i < s.Length && not find_end do
                match s.[i] with
                | '\\' ->
                    if i + 1 >= s.Length then
                        invalidOp $"incomplete escape for string"
                    else
                    match s.[i + 1] with
                    | 'b' -> ignore(buf.Append('\b'))
                    | 't' -> ignore(buf.Append('\t'))
                    | 'n' -> ignore(buf.Append('\n'))
                    | 'r' -> ignore(buf.Append('\r'))
                    | 'f' -> ignore(buf.Append('\f'))
                    | '\\' -> ignore(buf.Append('\\'))
                    | '"' -> ignore(buf.Append('"'))
                    | a -> ignore(buf.Append(a))
                    i <- i + 2
                | '"' ->
                    find_end <- true
                    i <- i + 1
                | a ->
                    ignore(buf.Append(a))
                    i <- i + 1
            if find_end then
                i, buf.ToString()
            else
                invalidOp "incomplete string"
        apply

    let pMap (f: 'a -> 'b) (p: Parser<'a>) : Parser<'b> =
        let apply i s =
            let i, v = p i s
            i, f v
        apply
    let pRef (p: Parser<'a> ref): Parser<'a> =
        let apply i s = p.Value i s
        apply

    module Json =
        let pListSep =
            pCharset [|','; ']'|]
            |> pMap (function
                | ',' -> true
                | ']' -> false
                | _ -> failwith "impossible")

        let pDictSep =
            pCharset [|','; '}'|]
            |> pMap (function
                | ',' -> true
                | '}' -> false
                | _ -> failwith "impossible")

        let jInt: Parser<int64> = pNumber |> pMap (fun s -> System.Int64.Parse(s))
        let jFloat: Parser<double> = pNumber |> pMap (fun s -> System.Double.Parse(s))

        let jNumber : Parser<Json> =
            let apply (i: int) (s: string) =
                if i >= s.Length then invalidOp "unexpected match"
                let start = i
                let rec loop isfloat j =
                    if j >= s.Length then isfloat, j
                    else
                    match s.[j] with
                    | '.' -> loop true (j + 1)
                    | 'E' | 'e' | '-' -> loop isfloat (j + 1)
                    | c when c <= '9'  && c >= '0' -> loop isfloat (j + 1)
                    | _ -> isfloat, j
                let isfloat, i = loop false i
                let o =
                    if isfloat then
                        JFloat(System.Double.Parse(s.[start..i-1]))
                    else
                        JInt(System.Int64.Parse(s.[start..i-1]))
                i, o
            apply

        let jTrue: Parser<bool> =
            pStr_ "true" |> pMap (fun s -> true)
        let jFalse: Parser<bool> =
            pStr_ "false" |> pMap (fun s -> false)
        let jNull: Parser<unit> = pStr_ "null"
        let jStr: Parser<string> = pStr

        let refObject: Parser<(string * Json) ResizeArray> ref = ref (Unchecked.defaultof<_>)
        let jObject = pRef refObject
        let refList: Parser<Json ResizeArray> ref = ref (Unchecked.defaultof<_>)
        let jList = pRef refList

        let json =
            la1 <| function
            | '[' -> jList |> pMap JList
            | '{' -> jObject |> pMap JDict
            | 't' -> jTrue |> pMap JBool
            | 'f' -> jFalse |> pMap JBool
            | 'n' -> jNull |> pMap (fun () -> JNull)
            | '-' -> jNumber
            | c when c >= '0' && c <= '9' -> jNumber
            | '"' -> jStr |> pMap JStr
            | c -> invalidOp (string c)


        refObject.Value <-
            fun (i: int) (s: string) ->
                let i, _ = pChar_ '{' i s
                let i, _ = pSpc i s
                if i >= s.Length then invalidOp "incomplete object"
                if s.[i] = '}' then i+1, ResizeArray<string * Json>()
                else
                let each i s =
                    let i, key = allowSPC jStr i s
                    let i, _ = allowSPC (pChar_ ':') i s
                    let i, v = allowSPC json i s
                    i, (key, v)
                pSepRep pDictSep each i s

        refList.Value <-
            fun (i: int) (s: string) ->
                let i, _ = pChar_ '[' i s
                let i, _ = pSpc i s
                if i >= s.Length then invalidOp "incomplete list"
                if s.[i] = ']' then i+1, ResizeArray<Json>()
                else
                pSepRep pListSep (allowSPC json) i s

let parseJson s =
    let i, o = (Parsec.allowSPC Parsec.Json.json) 0 s
    if i <> s.Length then invalidOp "json parse incomplete"
    else o


let int64FromJson =
    function
    | JInt i -> i
    | _ -> invalidOp "invalid conversion to int"

let doubleFromJson =
    function
    | JFloat f -> f
    | JInt i -> double i
    | _ -> invalidOp "invalid conversion to float"

let boolFromJson =
    function
    | JBool b -> b
    | _ -> invalidOp "invalid conversion to bool"

let stringFromJson =
    function
    | JStr s -> s
    | _ -> invalidOp "invalid conversion to string"

let charFromJson =
    function
    | JStr s when s.Length <> 1 -> invalidOp $"invalid interpretaion from string to char"
    | JStr s -> s.[0]
    | _ -> invalidOp "invalid conversion to char"


let unitFromJson =
    function
    | JInt 0L -> ()
    | _ -> invalidOp "invalid conversion to unit"


let inline forI f (seq: ResizeArray<'a>) =
    for i = 0 to seq.Count - 1 do
        f i (seq.[i])

let inline (==) a b = obj.ReferenceEquals(a, b)

let ADT_TAG = "_TAG"
let ADT_VALS = "_VALUES"

type 'a evidence = Evidence

let rec inline fromJson<'a> data =
    unbox<'a> (objFromJson (typeof<'a>) data)

and objFromJson (t: System.Type) (data: Json) =
    if obj.ReferenceEquals(typeof<int8>, t) then
        box <| int8 (int64FromJson data)
    elif obj.ReferenceEquals(typeof<int16>, t) then
        box <| int16 (int64FromJson data)
    elif obj.ReferenceEquals(typeof<int>, t) then
        box <| int (int64FromJson data)
    elif obj.ReferenceEquals(typeof<int64>, t) then
        box <| (int64FromJson data)

    elif obj.ReferenceEquals(typeof<float>, t) then
        box <| float (doubleFromJson data)
    elif obj.ReferenceEquals(typeof<double>, t) then
        box <| (doubleFromJson data)
    elif obj.ReferenceEquals(typeof<decimal>, t) then
        box <| (decimal <| doubleFromJson data)

    elif obj.ReferenceEquals(typeof<bool>, t) then
        box <| (boolFromJson data)
    elif obj.ReferenceEquals(typeof<char>, t) then
        let s = stringFromJson data
        if s.Length <> 1 then invalidOp $"{s} to char"
        else
            box <| s.[0]
    elif obj.ReferenceEquals(typeof<unit>, t) then
        box <| unitFromJson data
    elif obj.ReferenceEquals(typeof<string>, t) then
        box <| stringFromJson data
    elif t.IsArray then
        let eltype = t.GetElementType()
        let seq =
            match data with
            | JList seq -> seq
            | _ -> invalidOp $"convert {data.kind} to {t}"
        // integers
        if eltype == typeof<int> then
            box <| Array.init seq.Count (fun i -> int (int64FromJson seq.[i]))
        elif eltype == typeof<int64> then
            box <| Array.init seq.Count (fun i -> (int64FromJson seq.[i]))
        elif eltype == typeof<int16> then
            box <| Array.init seq.Count (fun i -> int16 (int64FromJson seq.[i]))
        elif eltype == typeof<int8> then
            box <| Array.init seq.Count (fun i -> int8 (int64FromJson seq.[i]))
        elif eltype == typeof<uint32> then
            box <| Array.init seq.Count (fun i -> Core.Operators.uint32 (int64FromJson seq.[i]))
        elif eltype == typeof<uint64> then
            box <| Array.init seq.Count (fun i -> Core.Operators.uint64 (int64FromJson seq.[i]))
        elif eltype == typeof<uint8> then
            box <| Array.init seq.Count (fun i -> Core.Operators.byte (int64FromJson seq.[i]))
        elif eltype == typeof<uint16> then
            box <| Array.init seq.Count (fun i -> Core.Operators.uint16 (int64FromJson seq.[i]))

        // floats
        elif eltype == typeof<float> then
            box <| Array.init seq.Count (fun i -> float (doubleFromJson seq.[i]))
        elif eltype == typeof<double> then
            box <| Array.init seq.Count (fun i -> (doubleFromJson seq.[i]))
        elif eltype == typeof<decimal>  then
            box <| Array.init seq.Count (fun i -> decimal (doubleFromJson seq.[i]))
        // others
        elif eltype == typeof<string> then
            box <| Array.init seq.Count (fun i -> (stringFromJson seq.[i]))
        elif eltype == typeof<bool> then
            box <| Array.init seq.Count (fun i -> (boolFromJson seq.[i]))
        elif eltype == typeof<unit> then
            box <| Array.init seq.Count (fun i -> (unitFromJson seq.[i]))
        elif eltype == typeof<char> then
            box <| Array.init seq.Count (fun i -> (charFromJson seq.[i]))
        else
            box <| Array.init seq.Count (fun i -> objFromJson eltype seq.[i])
        // let array = System.Array.CreateInstance(eltype, seq.Count)
        // for i = 0 to seq.Count - 1 do
        //     array.SetValue(objFromJson eltype (seq.[i]), i)
        // box <| array
    elif t.IsGenericType && t.GetGenericTypeDefinition() = typedefof<option<_>> then
        let eltype = t.GenericTypeArguments.[0]
        match data with
        | JNull -> None: obj
        | _ -> Some (objFromJson eltype data)
    elif t.IsGenericType && t.GetGenericTypeDefinition() = typedefof<System.Collections.Generic.List<_>> then
        let eltype = t.GenericTypeArguments.[0]
        let o = System.Collections.Generic.List<obj>()
        let seq =
            match data with
            | JList seq -> seq
            | _ -> invalidOp $"convert {data.kind} to {t}"
        for i = 0 to seq.Count - 1 do
            o.Add(objFromJson eltype seq.[i])
        box <| o
    elif t.IsGenericType && t.GetGenericTypeDefinition() = typedefof<list<_>> then
        let eltype = t.GenericTypeArguments.[0]
        let mutable o: obj list = []
        let seq =
            match data with
            | JList seq -> seq
            | _ -> invalidOp $"convert {data.kind} to {t}"
        for i = seq.Count - 1 downto 0 do
            o <- objFromJson eltype seq.[i] :: o
        box <| o
    elif FSharpType.IsRecord t then
        let fields = FSharpType.GetRecordFields t
                     |> Array.map (fun f -> f.Name, f.PropertyType)
        let arguments = Array.create fields.Length (null: obj)
        let pairs =
            match data with
            | JDict pairs -> pairs
            | _ -> invalidOp $"convert {data.kind} to {t}"
        for (k, v) in pairs do
            let i = Array.findIndex (fun (fname, _) -> k = fname) fields
            let (fieldname, fieldt) = fields.[i]
            try
                arguments.[i] <- objFromJson fieldt v
            with e ->
                invalidOp $"parsing {t.Name}.{fieldname}: {e}"

        FSharpValue.MakeRecord(t, arguments)
    elif FSharpType.IsTuple t then
        let eltypes = FSharpType.GetTupleElements t
        let seq =
            match data with
            | JList seq -> seq
            | _ -> invalidOp $"convert {data.kind} to {t}"
        FSharpValue.MakeTuple(
            Array.init seq.Count (fun i -> objFromJson eltypes.[i] seq.[i]), t)
    elif FSharpType.IsUnion t then
        let pairs =
            match data with
            | JDict pairs -> pairs
            | _ -> invalidOp $"convert {data.kind} to {t}"
        let _, tag = Seq.find (fun (k, _) -> k = ADT_TAG) pairs
        let tag = stringFromJson tag
        let _, values = Seq.find (fun (k, _) -> k = ADT_VALS) pairs
        let case =
            FSharpType.GetUnionCases t
            |> Array.find (fun case -> case.Name = tag)
        let fieldtypes = case.GetFields() |> Array.map (fun f -> f.PropertyType)
        let values =
            match values with
            | JList values -> Array.init values.Count (fun i -> objFromJson fieldtypes.[i] values.[i])
            | _ -> invalidOp $"convert {data.kind} to {t}"
        FSharpValue.MakeUnion(case, values)
    else
        invalidOp $"unsupported data type fromJson: {t}"


let rec objToJson (t: System.Type) (o: obj) =
    if obj.ReferenceEquals(typeof<int8>, t) then
        JInt (int64 <| unbox<int8> o)
    elif obj.ReferenceEquals(typeof<int16>, t) then
        JInt (int64 <| unbox<int16> o)
    elif obj.ReferenceEquals(typeof<int>, t) then
        JInt (unbox<int> o)
    elif obj.ReferenceEquals(typeof<int64>, t) then
        JInt (unbox<int64> o)
    elif obj.ReferenceEquals(typeof<float>, t) then
        JFloat (double <| unbox<float> o)
    elif obj.ReferenceEquals(typeof<double>, t) then
        JFloat (unbox<double> o)
    elif obj.ReferenceEquals(typeof<decimal>, t) then
        JFloat (double <| unbox<decimal> o)
    elif obj.ReferenceEquals(typeof<bool>, t) then
        JBool (unbox<bool> o)
    elif obj.ReferenceEquals(typeof<char>, t) then
        JStr (string <| unbox<char> o)
    elif obj.ReferenceEquals(typeof<unit>, t) then
        JInt 0
    elif obj.ReferenceEquals(typeof<string>, t) then
        JStr (unbox<string> o)
    elif t.IsArray then
        let eltype = t.GetElementType()


        // integers
        if eltype == typeof<int> then
            (unbox<array<int>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        elif eltype == typeof<int64> then
            (unbox<array<int64>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        elif eltype == typeof<int16> then
            (unbox<array<int16>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        elif eltype == typeof<int8> then
            (unbox<array<int8>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        elif eltype == typeof<uint32> then
            (unbox<array<uint32>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        elif eltype == typeof<uint64> then
            (unbox<array<uint64>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        elif eltype == typeof<uint8> then
            (unbox<array<uint8>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        elif eltype == typeof<uint16> then
            (unbox<array<uint16>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList

        // floats
        elif eltype == typeof<float> then
            (unbox<array<float>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        elif eltype == typeof<double> then
            (unbox<array<double>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        elif eltype == typeof<decimal>  then
            (unbox<array<decimal>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        // others
        elif eltype == typeof<string> then
            (unbox<array<string>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        elif eltype == typeof<bool> then
            (unbox<array<bool>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        elif eltype == typeof<unit> then
            (unbox<array<unit>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        elif eltype == typeof<char> then
            (unbox<array<char>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        else
            (unbox<array<obj>> o)
            |> Array.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
        // let array = System.Array.CreateInstance(eltype, seq.Count)
        // for i = 0 to seq.Count - 1 do
        //     array.SetValue(objFromJson eltype (seq.[i]), i)
        // box <| array
    elif t.IsGenericType && t.GetGenericTypeDefinition() = typedefof<option<_>> then
        let eltype = t.GenericTypeArguments.[0]
        match unbox<option<obj>>(o) with
        | None -> JNull
        | Some i -> objToJson eltype i
    elif t.IsGenericType && t.GetGenericTypeDefinition() = typedefof<list<_>> then
        let eltype = t.GenericTypeArguments.[0]
        (unbox<list<obj>> o)
            |> List.map (fun it -> objToJson eltype it)
            |> ResizeArray
            |> JList
    elif FSharpType.IsRecord t then
        let fields = FSharpType.GetRecordFields t
                     |> Array.map (fun f -> (f.Name, objToJson f.PropertyType (FSharpValue.GetRecordField(o, f))))
                     |> ResizeArray
        JDict fields
    elif FSharpType.IsTuple t then
        let eltypes = FSharpType.GetTupleElements t
        FSharpValue.GetTupleFields o
        |> Array.mapi (fun i e -> objToJson eltypes.[i] e)
        |> ResizeArray
        |> JList
    elif FSharpType.IsUnion t then
        let case, args = FSharpValue.GetUnionFields(o, t)
        let fieldtypes = case.GetFields() |> Array.map (fun f -> f.PropertyType)
        [|
            (ADT_TAG, JStr case.Name);
            (ADT_VALS,
                args
                |> Array.mapi (fun i e -> objToJson fieldtypes.[i] e)
                |> ResizeArray
                |> JList)
        |]
        |> ResizeArray
        |> JDict
    else
        invalidOp $"unsupported data type fromJson: {t}"

let escape_string (s : string) =
   let buf = System.Text.StringBuilder(s.Length)
   let rep c =
      match c with
      | '\\' -> buf.Append("\\\\")
      | '\r' -> buf.Append "\\r"
      | '\n' -> buf.Append "\\n"
      | '\t' -> buf.Append "\\t"
      | '\f' -> buf.Append "\\f"
      | '\b' -> buf.Append "\\b"
      | '"' -> buf.Append "\\\""
      | _ -> buf.Append c
   for i = 0 to s.Length - 1 do
       ignore(rep (s.[i]))
   buf.ToString()

let rec serializeJSON : Json -> string = fun x ->
    match x with
    | JInt i -> i.ToString()
    | JFloat f -> f.ToString()
    | JBool true -> "true"
    | JBool false -> "false"
    | JStr s -> "\"" + escape_string s + "\""
    | JNull -> "null"
    | JList seq ->
        "[" +  String.concat "," (Seq.map serializeJSON seq) + "]"
    | JDict pairs ->
        "{" +  String.concat "," (Seq.map (fun (k, v) ->
            "\"" + escape_string k + "\"" + ":" + serializeJSON v) pairs)
            + "}"





#if FABLE_COMPILER
let inline deserialize<'a> s =
    let json = parseJson s
    objFromJson typeof<'a> json :?> 'a

let inline serialize<'a> (a: 'a) =
    box a
    |> objToJson (typeof<'a>)
    |> serializeJSON
#else

let inline deserialize<'a> (s: string) = FSharp.Json.Json.deserialize<'a> s
let inline serialize<'a> (a: 'a): string = FSharp.Json.Json.serialize a

#endif