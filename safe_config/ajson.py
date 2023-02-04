from __future__ import annotations
from decimal import Decimal as Decimal_1
from typing import (Any, List, Tuple, Callable, TypeVar, Generic, Optional)
from .fable_modules.fable_library.array import (contains, initialize, map, fill, find_index, find as find_1, map_indexed)
from .fable_modules.fable_library.decimal import (Decimal, to_number as to_number_1)
from .fable_modules.fable_library.double import parse as parse_1
from .fable_modules.fable_library.list import (FSharpList, is_empty, head, tail, empty, cons, map as map_1)
from .fable_modules.fable_library.long import (parse, to_number, to_int, from_value, from_integer)
from .fable_modules.fable_library.option import (some, value as value_30)
from .fable_modules.fable_library.reflection import (TypeInfo, int64_type, float64_type, bool_type, string_type, array_type, tuple_type, union_type, int8_type, int16_type, int32_type, decimal_type, char_type, unit_type, is_array, get_element_type, uint32_type, uint64_type, uint8_type, uint16_type, is_generic_type, equals, get_generic_type_definition, obj_type, option_type, get_generics, list_type, is_record, name, get_record_elements, make_record, is_tuple, get_tuple_elements, make_tuple, is_union, get_union_cases, get_union_case_fields, make_union, get_record_field, get_tuple_fields, get_union_fields)
from .fable_modules.fable_library.seq import (find, map as map_2)
from .fable_modules.fable_library.string import join
from .fable_modules.fable_library.system_text import (StringBuilder__ctor, StringBuilder__Append_244C7CD6, StringBuilder__ctor_Z524259A4, StringBuilder__Append_Z721C83C5)
from .fable_modules.fable_library.types import (Array, Union, to_string, FSharpRef, int64, Int32Array, int16, Int16Array, int8, Int8Array, uint32, Uint32Array, uint64, uint8, Uint8Array, uint16, Uint16Array, Float64Array)
from .fable_modules.fable_library.util import (curry, string_hash, ignore, uncurry, get_enumerator, dispose, to_enumerable, int64_to_string)

_A = TypeVar("_A")

__A = TypeVar("__A")

_B = TypeVar("_B")

def _expr2() -> TypeInfo:
    return union_type("AJson.Json", [], Json, lambda: [[("Item", int64_type)], [("Item", float64_type)], [("Item", bool_type)], [("Item", string_type)], [], [("Item", array_type(Json_reflection()))], [("Item", array_type(tuple_type(string_type, Json_reflection())))]])


class Json(Union):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> List[str]:
        return ["JInt", "JFloat", "JBool", "JStr", "JNull", "JList", "JDict"]


Json_reflection = _expr2

def Json__get_kind(this: Json) -> str:
    if this.tag == 1:
        return "float"

    elif this.tag == 2:
        return "bool"

    elif this.tag == 3:
        return "string"

    elif this.tag == 4:
        return "null"

    elif this.tag == 5:
        return "list"

    elif this.tag == 6:
        return "dict"

    else: 
        return "int"



def Parsec_pChar_(c: str) -> Callable[[int, str], Tuple[int, None]]:
    def apply(i: int, s: str, c: str=c) -> Tuple[int, None]:
        if True if (i >= len(s)) else (s[i] != c):
            raise Exception("unexpected match")

        else: 
            return (i + 1, None)


    return curry(2, apply)


def Parsec_pStr_(pat: str) -> Callable[[int, str], Tuple[int, None]]:
    def apply(i: int, s: str, pat: str=pat) -> Tuple[int, None]:
        if True if ((i + len(pat)) > len(s)) else (s[i:((i + len(pat)) - 1) + 1] != pat):
            raise Exception("unexpected match")

        else: 
            return (i + len(pat), None)


    return curry(2, apply)


def Parsec_pChar(c: str) -> Callable[[int, str], Tuple[int, str]]:
    def apply(i: int, s: str, c: str=c) -> Tuple[int, str]:
        if True if (i >= len(s)) else (s[i] != c):
            raise Exception("unexpected match")

        else: 
            return (i + 1, c)


    return curry(2, apply)


def Parsec_pCharset_(cs: Array[str]) -> Callable[[int, str], Tuple[int, None]]:
    def apply(i: int, s: str, cs: Any=cs) -> Tuple[int, None]:
        if i >= len(s):
            raise Exception("unexpected match")

        else: 
            class ObjectExpr4:
                @property
                def Equals(self) -> Callable[[str, str], bool]:
                    def _arrow3(x: str, y: str) -> bool:
                        return x == y

                    return _arrow3

                @property
                def GetHashCode(self) -> Callable[[str], int]:
                    return string_hash

            if contains(s[i], cs, ObjectExpr4()):
                return (i + 1, None)

            else: 
                raise Exception("unexpected match")



    return curry(2, apply)


def Parsec_pCharset(cs: Array[str]) -> Callable[[int, str], Tuple[int, str]]:
    def apply(i: int, s: str, cs: Any=cs) -> Tuple[int, str]:
        if i >= len(s):
            raise Exception("unexpected match")

        else: 
            class ObjectExpr6:
                @property
                def Equals(self) -> Callable[[str, str], bool]:
                    def _arrow5(x: str, y: str) -> bool:
                        return x == y

                    return _arrow5

                @property
                def GetHashCode(self) -> Callable[[str], int]:
                    return string_hash

            if contains(s[i], cs, ObjectExpr6()):
                return (i + 1, s[i])

            else: 
                raise Exception(("unexpected match " + str(s[i])) + "")



    return curry(2, apply)


def Parsec_pIgnore(p: Callable[[int, str], Tuple[int, _A]]) -> Callable[[int, str], Tuple[int, None]]:
    def apply(i: int, s: str, p: Any=p) -> Tuple[int, None]:
        return (p(i, s)[0], None)

    return curry(2, apply)


def Parsec_pSeq_(ps: FSharpList[Callable[[int, str], Tuple[int, None]]]) -> Callable[[int, str], Tuple[int, None]]:
    def apply(i: int, s: str, ps: Any=ps) -> Tuple[int, None]:
        def loop(i_1_mut: int, ps_1_mut: FSharpList[Callable[[int, str], Tuple[int, __A]]], i: int=i, s: str=s) -> Tuple[int, None]:
            while True:
                (i_1, ps_1) = (i_1_mut, ps_1_mut)
                if i_1 >= len(s):
                    raise Exception("unexpected match")

                elif is_empty(ps_1):
                    return (i_1, None)

                else: 
                    i_1_mut = head(ps_1)(i_1)(s)[0]
                    ps_1_mut = tail(ps_1)
                    continue

                break

        return loop(i, ps)

    return curry(2, apply)


def Parsec_pSepRep(sep: Callable[[int, str], Tuple[int, bool]], p: Callable[[int, str], Tuple[int, _A]]) -> Callable[[int, str], Tuple[int, Array[_A]]]:
    def apply(i: int, s: str, sep: Any=sep, p: Any=p) -> Tuple[int, Array[_A]]:
        res: Array[_A] = []
        def loop(i_1_mut: int, i: int=i, s: str=s) -> Tuple[int, Array[_A]]:
            while True:
                (i_1,) = (i_1_mut,)
                if i_1 >= len(s):
                    raise Exception("unexpected match")

                else: 
                    pattern_input: Tuple[int, _A] = p(i_1, s)
                    (res.append(pattern_input[1]))
                    pattern_input_1: Tuple[int, bool] = sep(pattern_input[0], s)
                    i_3: int = pattern_input_1[0] or 0
                    if pattern_input_1[1]:
                        i_1_mut = i_3
                        continue

                    else: 
                        return (i_3, res)


                break

        return loop(i)

    return curry(2, apply)


def _arrow7(__unit: None=None) -> Callable[[int, str], Tuple[int, None]]:
    def apply(i: int, s: str) -> Tuple[int, None]:
        def loop(i_1_mut: int, i: int=i, s: str=s) -> Tuple[int, None]:
            while True:
                (i_1,) = (i_1_mut,)
                if i_1 >= len(s):
                    return (i_1, None)

                else: 
                    match_value: str = s[i_1]
                    (pattern_matching_result,) = (None,)
                    if match_value == "\t":
                        pattern_matching_result = 0

                    elif match_value == "\n":
                        pattern_matching_result = 0

                    elif match_value == "\r":
                        pattern_matching_result = 0

                    elif match_value == " ":
                        pattern_matching_result = 0

                    else: 
                        pattern_matching_result = 1

                    if pattern_matching_result == 0:
                        i_1_mut = i_1 + 1
                        continue

                    elif pattern_matching_result == 1:
                        return (i_1, None)


                break

        return loop(i)

    return curry(2, apply)


Parsec_pSpc: Callable[[int, str], Tuple[int, None]] = _arrow7()

def Parsec_allowSPC(p: Callable[[int, str], Tuple[int, _A]]) -> Callable[[int, str], Tuple[int, _A]]:
    def apply(i: int, s: str, p: Any=p) -> Tuple[int, _A]:
        pattern_input_1: Tuple[int, _A] = p(Parsec_pSpc(i)(s)[0], s)
        return (Parsec_pSpc(pattern_input_1[0])(s)[0], pattern_input_1[1])

    return curry(2, apply)


def Parsec_la1(dispatch: Callable[[str, int, str], Tuple[int, _A]]) -> Callable[[int, str], Tuple[int, _A]]:
    def apply(i: int, s: str, dispatch: Any=dispatch) -> Tuple[int, _A]:
        if i >= len(s):
            raise Exception("unexpected match")

        return dispatch(s[i], i, s)

    return curry(2, apply)


def _arrow9(__unit: None=None) -> Callable[[int, str], Tuple[int, str]]:
    def apply(i: int, s: str) -> Tuple[int, str]:
        if i >= len(s):
            raise Exception("unexpected match")

        def loop(j_mut: int, i: int=i, s: str=s) -> int:
            while True:
                (j,) = (j_mut,)
                if j >= len(s):
                    return j

                else: 
                    match_value: str = s[j]
                    (pattern_matching_result,) = (None,)
                    if match_value == "-":
                        pattern_matching_result = 0

                    elif match_value == ".":
                        pattern_matching_result = 0

                    elif match_value == "E":
                        pattern_matching_result = 0

                    elif match_value == "e":
                        pattern_matching_result = 0

                    else: 
                        def _arrow8(__unit: None=None, j: int=j) -> bool:
                            c: str = match_value
                            return (c >= "0") if (c <= "9") else False

                        if _arrow8():
                            pattern_matching_result = 1

                        else: 
                            pattern_matching_result = 2


                    if pattern_matching_result == 0:
                        j_mut = j + 1
                        continue

                    elif pattern_matching_result == 1:
                        j_mut = j + 1
                        continue

                    elif pattern_matching_result == 2:
                        return j


                break

        i_1: int = loop(i) or 0
        return (i_1, s[i:(i_1 - 1) + 1])

    return curry(2, apply)


Parsec_pNumber: Callable[[int, str], Tuple[int, str]] = _arrow9()

def _arrow10(__unit: None=None) -> Callable[[int, str], Tuple[int, str]]:
    def apply(i: int, s: str) -> Tuple[int, str]:
        if True if (i >= len(s)) else (s[i] != "\""):
            raise Exception("incomplete parsing for string")

        buf: Any = StringBuilder__ctor()
        find_end: bool = False
        i_1: int = (i + 1) or 0
        while (not find_end) if (i_1 < len(s)) else False:
            match_value: str = s[i_1]
            if match_value == "\"":
                find_end = True
                i_1 = (i_1 + 1) or 0

            elif match_value == "\\":
                if (i_1 + 1) >= len(s):
                    raise Exception("incomplete escape for string")

                else: 
                    match_value_1: str = s[i_1 + 1]
                    if match_value_1 == "\"":
                        ignore(StringBuilder__Append_244C7CD6(buf, "\""))

                    elif match_value_1 == "\\":
                        ignore(StringBuilder__Append_244C7CD6(buf, "\\"))

                    elif match_value_1 == "b":
                        ignore(StringBuilder__Append_244C7CD6(buf, "\b"))

                    elif match_value_1 == "f":
                        ignore(StringBuilder__Append_244C7CD6(buf, "\f"))

                    elif match_value_1 == "n":
                        ignore(StringBuilder__Append_244C7CD6(buf, "\n"))

                    elif match_value_1 == "r":
                        ignore(StringBuilder__Append_244C7CD6(buf, "\r"))

                    elif match_value_1 == "t":
                        ignore(StringBuilder__Append_244C7CD6(buf, "\t"))

                    else: 
                        ignore(StringBuilder__Append_244C7CD6(buf, match_value_1))

                    i_1 = (i_1 + 2) or 0


            else: 
                ignore(StringBuilder__Append_244C7CD6(buf, match_value))
                i_1 = (i_1 + 1) or 0

        if find_end:
            return (i_1, to_string(buf))

        else: 
            raise Exception("incomplete string")


    return curry(2, apply)


Parsec_pStr: Callable[[int, str], Tuple[int, str]] = _arrow10()

def Parsec_pMap(f: Callable[[_A], _B], p: Callable[[int, str], Tuple[int, _A]]) -> Callable[[int, str], Tuple[int, _B]]:
    def apply(i: int, s: str, f: Any=f, p: Any=p) -> Tuple[int, _B]:
        pattern_input: Tuple[int, _A] = p(i, s)
        return (pattern_input[0], f(pattern_input[1]))

    return curry(2, apply)


def Parsec_pRef(p: FSharpRef[Callable[[int, str], Tuple[int, _A]]]) -> Callable[[int, str], Tuple[int, _A]]:
    def apply(i: int, s: str, p: Any=p) -> Tuple[int, _A]:
        return p.contents(i)(s)

    return curry(2, apply)


def f(_arg: str) -> bool:
    if _arg == ",":
        return True

    elif _arg == "]":
        return False

    else: 
        raise Exception("impossible")



Parsec_Json_pListSep: Callable[[int, str], Tuple[int, bool]] = Parsec_pMap(f, uncurry(2, Parsec_pCharset([",", "]"])))

def f(_arg: str) -> bool:
    if _arg == ",":
        return True

    elif _arg == "}":
        return False

    else: 
        raise Exception("impossible")



Parsec_Json_pDictSep: Callable[[int, str], Tuple[int, bool]] = Parsec_pMap(f, uncurry(2, Parsec_pCharset([",", "}"])))

def f(s: str) -> int64:
    return parse(s, 511, False, 64)


Parsec_Json_jInt: Callable[[int, str], Tuple[int, int64]] = Parsec_pMap(f, uncurry(2, Parsec_pNumber))

Parsec_Json_jFloat: Callable[[int, str], Tuple[int, float]] = Parsec_pMap(parse_1, uncurry(2, Parsec_pNumber))

def _arrow12(__unit: None=None) -> Callable[[int, str], Tuple[int, Json]]:
    def apply(i: int, s: str) -> Tuple[int, Json]:
        if i >= len(s):
            raise Exception("unexpected match")

        start: int = i or 0
        def loop(isfloat_mut: bool, j_mut: int, i: int=i, s: str=s) -> Tuple[bool, int]:
            while True:
                (isfloat, j) = (isfloat_mut, j_mut)
                if j >= len(s):
                    return (isfloat, j)

                else: 
                    match_value: str = s[j]
                    (pattern_matching_result,) = (None,)
                    if match_value == "-":
                        pattern_matching_result = 1

                    elif match_value == ".":
                        pattern_matching_result = 0

                    elif match_value == "E":
                        pattern_matching_result = 1

                    elif match_value == "e":
                        pattern_matching_result = 1

                    else: 
                        def _arrow11(__unit: None=None, isfloat: bool=isfloat, j: int=j) -> bool:
                            c: str = match_value
                            return (c >= "0") if (c <= "9") else False

                        if _arrow11():
                            pattern_matching_result = 2

                        else: 
                            pattern_matching_result = 3


                    if pattern_matching_result == 0:
                        isfloat_mut = True
                        j_mut = j + 1
                        continue

                    elif pattern_matching_result == 1:
                        isfloat_mut = isfloat
                        j_mut = j + 1
                        continue

                    elif pattern_matching_result == 2:
                        isfloat_mut = isfloat
                        j_mut = j + 1
                        continue

                    elif pattern_matching_result == 3:
                        return (isfloat, j)


                break

        pattern_input: Tuple[bool, int] = loop(False, i)
        i_1: int = pattern_input[1] or 0
        return (i_1, Json(1, parse_1(s[start:(i_1 - 1) + 1])) if pattern_input[0] else Json(0, parse(s[start:(i_1 - 1) + 1], 511, False, 64)))

    return curry(2, apply)


Parsec_Json_jNumber: Callable[[int, str], Tuple[int, Json]] = _arrow12()

def f(__unit: None=None) -> bool:
    return True


Parsec_Json_jTrue: Callable[[int, str], Tuple[int, bool]] = Parsec_pMap(f, uncurry(2, Parsec_pStr_("true")))

def f(__unit: None=None) -> bool:
    return False


Parsec_Json_jFalse: Callable[[int, str], Tuple[int, bool]] = Parsec_pMap(f, uncurry(2, Parsec_pStr_("false")))

Parsec_Json_jNull: Callable[[int, str], Tuple[int, None]] = Parsec_pStr_("null")

Parsec_Json_jStr: Callable[[int, str], Tuple[int, str]] = Parsec_pStr

Parsec_Json_refObject: FSharpRef[Callable[[int, str], Tuple[int, Array[Tuple[str, Json]]]]] = FSharpRef(None)

Parsec_Json_jObject: Callable[[int, str], Tuple[int, Array[Tuple[str, Json]]]] = Parsec_pRef(Parsec_Json_refObject)

Parsec_Json_refList: FSharpRef[Callable[[int, str], Tuple[int, Array[Json]]]] = FSharpRef(None)

Parsec_Json_jList: Callable[[int, str], Tuple[int, Array[Json]]] = Parsec_pRef(Parsec_Json_refList)

def _arrow15(_arg: str) -> Callable[[int, str], Tuple[int, Json]]:
    (pattern_matching_result,) = (None,)
    if _arg == "\"":
        def _arrow13(__unit: None=None) -> bool:
            c: str = _arg
            return (c <= "9") if (c >= "0") else False

        if _arrow13():
            pattern_matching_result = 6

        else: 
            pattern_matching_result = 7


    elif _arg == "-":
        pattern_matching_result = 5

    elif _arg == "[":
        pattern_matching_result = 0

    elif _arg == "f":
        pattern_matching_result = 3

    elif _arg == "n":
        pattern_matching_result = 4

    elif _arg == "t":
        pattern_matching_result = 2

    elif _arg == "{":
        pattern_matching_result = 1

    else: 
        def _arrow14(__unit: None=None) -> bool:
            c_1: str = _arg
            return (c_1 <= "9") if (c_1 >= "0") else False

        if _arrow14():
            pattern_matching_result = 6

        else: 
            pattern_matching_result = 8


    if pattern_matching_result == 0:
        def f(arg: Array[Json]) -> Json:
            return Json(5, arg)

        return Parsec_pMap(f, uncurry(2, Parsec_Json_jList))

    elif pattern_matching_result == 1:
        def f_1(arg_1: Array[Tuple[str, Json]]) -> Json:
            return Json(6, arg_1)

        return Parsec_pMap(f_1, uncurry(2, Parsec_Json_jObject))

    elif pattern_matching_result == 2:
        def f_2(arg_2: bool) -> Json:
            return Json(2, arg_2)

        return Parsec_pMap(f_2, uncurry(2, Parsec_Json_jTrue))

    elif pattern_matching_result == 3:
        def f_3(arg_3: bool) -> Json:
            return Json(2, arg_3)

        return Parsec_pMap(f_3, uncurry(2, Parsec_Json_jFalse))

    elif pattern_matching_result == 4:
        def f_4(__unit: None=None) -> Json:
            return Json(4)

        return Parsec_pMap(f_4, uncurry(2, Parsec_Json_jNull))

    elif pattern_matching_result == 5:
        return Parsec_Json_jNumber

    elif pattern_matching_result == 6:
        return Parsec_Json_jNumber

    elif pattern_matching_result == 7:
        def f_5(arg_4: str) -> Json:
            return Json(3, arg_4)

        return Parsec_pMap(f_5, uncurry(2, Parsec_Json_jStr))

    elif pattern_matching_result == 8:
        raise Exception(_arg)



Parsec_Json_json: Callable[[int, str], Tuple[int, Json]] = Parsec_la1(uncurry(3, _arrow15))

def _arrow17(i: int) -> Callable[[str], Tuple[int, Array[Tuple[str, Json]]]]:
    def _arrow16(s: str) -> Tuple[int, Array[Tuple[str, Json]]]:
        i_2: int = Parsec_pSpc(Parsec_pChar_("{")(i)(s)[0])(s)[0] or 0
        if i_2 >= len(s):
            raise Exception("incomplete object")

        if s[i_2] == "}":
            return (i_2 + 1, [])

        else: 
            def each(i_3: int, s_1: str) -> Tuple[int, Tuple[str, Json]]:
                pattern_input_2: Tuple[int, str] = Parsec_allowSPC(uncurry(2, Parsec_Json_jStr))(i_3)(s_1)
                pattern_input_3: Tuple[int, None] = Parsec_allowSPC(uncurry(2, Parsec_pChar_(":")))(pattern_input_2[0])(s_1)
                pattern_input_4: Tuple[int, Json] = Parsec_allowSPC(uncurry(2, Parsec_Json_json))(pattern_input_3[0])(s_1)
                return (pattern_input_4[0], (pattern_input_2[1], pattern_input_4[1]))

            return Parsec_pSepRep(uncurry(2, Parsec_Json_pDictSep), each)(i_2)(s)


    return _arrow16


Parsec_Json_refObject.contents = _arrow17

def _arrow19(i: int) -> Callable[[str], Tuple[int, Array[Json]]]:
    def _arrow18(s: str) -> Tuple[int, Array[Json]]:
        i_2: int = Parsec_pSpc(Parsec_pChar_("[")(i)(s)[0])(s)[0] or 0
        if i_2 >= len(s):
            raise Exception("incomplete list")

        return ((i_2 + 1, [])) if (s[i_2] == "]") else Parsec_pSepRep(uncurry(2, Parsec_Json_pListSep), uncurry(2, Parsec_allowSPC(uncurry(2, Parsec_Json_json))))(i_2)(s)

    return _arrow18


Parsec_Json_refList.contents = _arrow19

def parse_json(s: str) -> Json:
    pattern_input: Tuple[int, Json] = Parsec_allowSPC(uncurry(2, Parsec_Json_json))(0)(s)
    if pattern_input[0] != len(s):
        raise Exception("json parse incomplete")

    else: 
        return pattern_input[1]



def int64from_json(_arg: Json) -> int64:
    if _arg.tag == 0:
        return _arg.fields[0]

    else: 
        raise Exception("invalid conversion to int")



def double_from_json(_arg: Json) -> float:
    if _arg.tag == 1:
        return _arg.fields[0]

    elif _arg.tag == 0:
        return to_number(_arg.fields[0])

    else: 
        raise Exception("invalid conversion to float")



def bool_from_json(_arg: Json) -> bool:
    if _arg.tag == 2:
        return _arg.fields[0]

    else: 
        raise Exception("invalid conversion to bool")



def string_from_json(_arg: Json) -> str:
    if _arg.tag == 3:
        return _arg.fields[0]

    else: 
        raise Exception("invalid conversion to string")



def char_from_json(_arg: Json) -> str:
    if _arg.tag == 3:
        if len(_arg.fields[0]) != 1:
            raise Exception("invalid interpretaion from string to char")

        else: 
            return _arg.fields[0][0]


    else: 
        raise Exception("invalid conversion to char")



def unit_from_json(_arg: Json) -> None:
    (pattern_matching_result,) = (None,)
    if _arg.tag == 0:
        if _arg.fields[0] == int64(0):
            pattern_matching_result = 0

        else: 
            pattern_matching_result = 1


    else: 
        pattern_matching_result = 1

    if pattern_matching_result == 0:
        pass

    elif pattern_matching_result == 1:
        raise Exception("invalid conversion to unit")



ADT_TAG: str = "_TAG"

ADT_VALS: str = "_VALUES"

def _expr20(gen0: TypeInfo) -> TypeInfo:
    return union_type("AJson.evidence`1", [gen0], evidence_1, lambda: [[]])


class evidence_1(Union, Generic[_A]):
    def __init__(self, tag: int, *fields: Any) -> None:
        super().__init__()
        self.tag: int = tag or 0
        self.fields: Array[Any] = list(fields)

    @staticmethod
    def cases() -> List[str]:
        return ["Evidence"]


evidence_1_reflection = _expr20

def obj_from_json(t: Any, data: Json) -> Any:
    if int8_type is t:
        return (int(to_int(int64from_json(data))) + 0x80 & 0xFF) - 0x80

    elif int16_type is t:
        return (int(to_int(int64from_json(data))) + 0x8000 & 0xFFFF) - 0x8000

    elif int32_type is t:
        return int(to_int(int64from_json(data)))

    elif int64_type is t:
        return int64from_json(data)

    elif float64_type is t:
        return double_from_json(data)

    elif float64_type is t:
        return double_from_json(data)

    elif decimal_type is t:
        return Decimal(double_from_json(data))

    elif bool_type is t:
        return bool_from_json(data)

    elif char_type is t:
        s: str = string_from_json(data)
        if len(s) != 1:
            raise Exception(("" + s) + " to char")

        else: 
            return s[0]


    elif unit_type is t:
        value_10: None = unit_from_json(data)
        return None

    elif string_type is t:
        return string_from_json(data)

    elif is_array(t):
        eltype: Any = get_element_type(t)
        seq_1: Array[Json]
        if data.tag == 5:
            seq_1 = data.fields[0]

        else: 
            raise Exception(((("convert " + Json__get_kind(data)) + " to ") + str(t)) + "")

        if eltype is int32_type:
            def _arrow21(i: int, t: Any=t, data: Json=data) -> int:
                return int(to_int(int64from_json(seq_1[i])))

            return initialize(len(seq_1), _arrow21, Int32Array)

        elif eltype is int64_type:
            def _arrow22(i_1: int, t: Any=t, data: Json=data) -> int64:
                return int64from_json(seq_1[i_1])

            return initialize(len(seq_1), _arrow22, None)

        elif eltype is int16_type:
            def _arrow23(i_2: int, t: Any=t, data: Json=data) -> int16:
                return (int(to_int(int64from_json(seq_1[i_2]))) + 0x8000 & 0xFFFF) - 0x8000

            return initialize(len(seq_1), _arrow23, Int16Array)

        elif eltype is int8_type:
            def _arrow24(i_3: int, t: Any=t, data: Json=data) -> int8:
                return (int(to_int(int64from_json(seq_1[i_3]))) + 0x80 & 0xFF) - 0x80

            return initialize(len(seq_1), _arrow24, Int8Array)

        elif eltype is uint32_type:
            def _arrow25(i_4: int, t: Any=t, data: Json=data) -> uint32:
                return int(to_int(int64from_json(seq_1[i_4]))+0x100000000 if to_int(int64from_json(seq_1[i_4])) < 0 else to_int(int64from_json(seq_1[i_4])))

            return initialize(len(seq_1), _arrow25, Uint32Array)

        elif eltype is uint64_type:
            def _arrow26(i_5: int, t: Any=t, data: Json=data) -> uint64:
                return from_value(int64from_json(seq_1[i_5]), True)

            return initialize(len(seq_1), _arrow26, None)

        elif eltype is uint8_type:
            def _arrow27(i_6: int, t: Any=t, data: Json=data) -> uint8:
                return int(to_int(int64from_json(seq_1[i_6]))+0x100 if to_int(int64from_json(seq_1[i_6])) < 0 else to_int(int64from_json(seq_1[i_6]))) & 0xFF

            return initialize(len(seq_1), _arrow27, Uint8Array)

        elif eltype is uint16_type:
            def _arrow28(i_7: int, t: Any=t, data: Json=data) -> uint16:
                return int(to_int(int64from_json(seq_1[i_7]))+0x10000 if to_int(int64from_json(seq_1[i_7])) < 0 else to_int(int64from_json(seq_1[i_7]))) & 0xFFFF

            return initialize(len(seq_1), _arrow28, Uint16Array)

        elif eltype is float64_type:
            def _arrow29(i_8: int, t: Any=t, data: Json=data) -> float:
                return double_from_json(seq_1[i_8])

            return initialize(len(seq_1), _arrow29, Float64Array)

        elif eltype is float64_type:
            def _arrow30(i_9: int, t: Any=t, data: Json=data) -> float:
                return double_from_json(seq_1[i_9])

            return initialize(len(seq_1), _arrow30, Float64Array)

        elif eltype is decimal_type:
            def _arrow31(i_10: int, t: Any=t, data: Json=data) -> Decimal_1:
                return Decimal(double_from_json(seq_1[i_10]))

            return initialize(len(seq_1), _arrow31, None)

        elif eltype is string_type:
            def _arrow32(i_11: int, t: Any=t, data: Json=data) -> str:
                return string_from_json(seq_1[i_11])

            return initialize(len(seq_1), _arrow32, None)

        elif eltype is bool_type:
            def _arrow33(i_12: int, t: Any=t, data: Json=data) -> bool:
                return bool_from_json(seq_1[i_12])

            return initialize(len(seq_1), _arrow33, None)

        elif eltype is unit_type:
            def _arrow34(i_13: int, t: Any=t, data: Json=data) -> None:
                unit_from_json(seq_1[i_13])

            return initialize(len(seq_1), _arrow34, None)

        elif eltype is char_type:
            def _arrow35(i_14: int, t: Any=t, data: Json=data) -> str:
                return char_from_json(seq_1[i_14])

            return initialize(len(seq_1), _arrow35, None)

        else: 
            def _arrow36(i_15: int, t: Any=t, data: Json=data) -> Any:
                return obj_from_json(eltype, seq_1[i_15])

            return initialize(len(seq_1), _arrow36, None)


    elif equals(get_generic_type_definition(t), option_type(obj_type)) if is_generic_type(t) else False:
        if data.tag == 4:
            return None

        else: 
            return some(obj_from_json(get_generics(t)[0], data))


    elif equals(get_generic_type_definition(t), array_type(obj_type)) if is_generic_type(t) else False:
        o: Array[Any] = []
        seq_3: Array[Json]
        if data.tag == 5:
            seq_3 = data.fields[0]

        else: 
            raise Exception(((("convert " + Json__get_kind(data)) + " to ") + str(t)) + "")

        for i_16 in range(0, (len(seq_3) - 1) + 1, 1):
            (o.append(obj_from_json(get_generics(t)[0], seq_3[i_16])))
        return o

    elif equals(get_generic_type_definition(t), list_type(obj_type)) if is_generic_type(t) else False:
        o_1: FSharpList[Any] = empty()
        seq_5: Array[Json]
        if data.tag == 5:
            seq_5 = data.fields[0]

        else: 
            raise Exception(((("convert " + Json__get_kind(data)) + " to ") + str(t)) + "")

        for i_17 in range(len(seq_5) - 1, 0 - 1, -1):
            o_1 = cons(obj_from_json(get_generics(t)[0], seq_5[i_17]), o_1)
        return o_1

    elif is_record(t):
        def mapping(f: Any, t: Any=t, data: Json=data) -> Tuple[str, Any]:
            return (name(f), f[1])

        fields: Array[Tuple[str, Any]] = map(mapping, get_record_elements(t), None)
        arguments: Array[Any] = fill([0] * len(fields), 0, len(fields), None)
        def _arrow37(__unit: None=None, t: Any=t, data: Json=data) -> Array[Tuple[str, Json]]:
            raise Exception(((("convert " + Json__get_kind(data)) + " to ") + str(t)) + "")

        enumerator: Any = get_enumerator(data.fields[0] if (data.tag == 6) else _arrow37())
        try: 
            while enumerator.System_Collections_IEnumerator_MoveNext():
                for_loop_var: Tuple[str, Json] = enumerator.System_Collections_Generic_IEnumerator_1_get_Current()
                def _arrow38(tupled_arg: Tuple[str, Any]) -> bool:
                    return for_loop_var[0] == tupled_arg[0]

                i_18: int = find_index(_arrow38, fields) or 0
                pattern_input: Tuple[str, Any] = fields[i_18]
                try: 
                    arguments[i_18] = obj_from_json(pattern_input[1], for_loop_var[1])

                except Exception as e:
                    raise Exception(((((("parsing " + name(t)) + ".") + pattern_input[0]) + ": ") + str(e)) + "")


        finally: 
            dispose(enumerator)

        return make_record(t, arguments)

    elif is_tuple(t):
        eltypes: Array[Any] = get_tuple_elements(t)
        seq_7: Array[Json]
        if data.tag == 5:
            seq_7 = data.fields[0]

        else: 
            raise Exception(((("convert " + Json__get_kind(data)) + " to ") + str(t)) + "")

        def _arrow39(i_19: int, t: Any=t, data: Json=data) -> Any:
            return obj_from_json(eltypes[i_19], seq_7[i_19])

        return make_tuple(initialize(len(seq_7), _arrow39, None), t)

    elif is_union(t):
        pairs_3: Array[Tuple[str, Json]]
        if data.tag == 6:
            pairs_3 = data.fields[0]

        else: 
            raise Exception(((("convert " + Json__get_kind(data)) + " to ") + str(t)) + "")

        def _arrow40(tupled_arg_1: Tuple[str, Json], t: Any=t, data: Json=data) -> bool:
            return tupled_arg_1[0] == ADT_TAG

        tag_1: str = string_from_json(find(_arrow40, pairs_3)[1])
        def _arrow41(tupled_arg_2: Tuple[str, Json], t: Any=t, data: Json=data) -> bool:
            return tupled_arg_2[0] == ADT_VALS

        values: Json = find(_arrow41, pairs_3)[1]
        def predicate(case: Any, t: Any=t, data: Json=data) -> bool:
            return name(case) == tag_1

        case_1: Any = find_1(predicate, get_union_cases(t))
        def mapping_1(f_1: Any, t: Any=t, data: Json=data) -> Any:
            return f_1[1]

        fieldtypes: Array[Any] = map(mapping_1, get_union_case_fields(case_1), None)
        def _arrow43(__unit: None=None, t: Any=t, data: Json=data) -> Array[Any]:
            values_1: Array[Json] = values.fields[0]
            def _arrow42(i_20: int) -> Any:
                return obj_from_json(fieldtypes[i_20], values_1[i_20])

            return initialize(len(values_1), _arrow42, None)

        def _arrow44(__unit: None=None, t: Any=t, data: Json=data) -> Array[Any]:
            raise Exception(((("convert " + Json__get_kind(data)) + " to ") + str(t)) + "")

        return make_union(case_1, _arrow43() if (values.tag == 5) else _arrow44())

    else: 
        raise Exception(("unsupported data type fromJson: " + str(t)) + "")



def obj_to_json(t_mut: Any, o_mut: Any) -> Json:
    while True:
        (t, o) = (t_mut, o_mut)
        if int8_type is t:
            return Json(0, from_integer(o, False, 0))

        elif int16_type is t:
            return Json(0, from_integer(o, False, 1))

        elif int32_type is t:
            return Json(0, from_integer(o, False, 2))

        elif int64_type is t:
            return Json(0, o)

        elif float64_type is t:
            return Json(1, o)

        elif float64_type is t:
            return Json(1, o)

        elif decimal_type is t:
            return Json(1, to_number_1(o))

        elif bool_type is t:
            return Json(2, o)

        elif char_type is t:
            return Json(3, o)

        elif unit_type is t:
            return Json(0, from_integer(0, False, 2))

        elif string_type is t:
            return Json(3, o)

        elif is_array(t):
            eltype: Any = get_element_type(t)
            if eltype is int32_type:
                def mapping(it: int, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it)

                return Json(5, list(map(mapping, o, None)))

            elif eltype is int64_type:
                def mapping_1(it_1: int64, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_1)

                return Json(5, list(map(mapping_1, o, None)))

            elif eltype is int16_type:
                def mapping_2(it_2: int16, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_2)

                return Json(5, list(map(mapping_2, o, None)))

            elif eltype is int8_type:
                def mapping_3(it_3: int8, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_3)

                return Json(5, list(map(mapping_3, o, None)))

            elif eltype is uint32_type:
                def mapping_4(it_4: uint32, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_4)

                return Json(5, list(map(mapping_4, o, None)))

            elif eltype is uint64_type:
                def mapping_5(it_5: uint64, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_5)

                return Json(5, list(map(mapping_5, o, None)))

            elif eltype is uint8_type:
                def mapping_6(it_6: uint8, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_6)

                return Json(5, list(map(mapping_6, o, None)))

            elif eltype is uint16_type:
                def mapping_7(it_7: uint16, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_7)

                return Json(5, list(map(mapping_7, o, None)))

            elif eltype is float64_type:
                def mapping_8(it_8: float, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_8)

                return Json(5, list(map(mapping_8, o, None)))

            elif eltype is float64_type:
                def mapping_9(it_9: float, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_9)

                return Json(5, list(map(mapping_9, o, None)))

            elif eltype is decimal_type:
                def mapping_10(it_10: Decimal_1, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_10)

                return Json(5, list(map(mapping_10, o, None)))

            elif eltype is string_type:
                def mapping_11(it_11: str, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_11)

                return Json(5, list(map(mapping_11, o, None)))

            elif eltype is bool_type:
                def mapping_12(it_12: bool, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_12)

                return Json(5, list(map(mapping_12, o, None)))

            elif eltype is unit_type:
                def mapping_13(__unit: None=None, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, None)

                return Json(5, list(map(mapping_13, o, None)))

            elif eltype is char_type:
                def mapping_14(it_14: str, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_14)

                return Json(5, list(map(mapping_14, o, None)))

            else: 
                def mapping_15(it_15: Any=None, t: Any=t, o: Any=o) -> Json:
                    return obj_to_json(eltype, it_15)

                return Json(5, list(map(mapping_15, o, None)))


        elif equals(get_generic_type_definition(t), option_type(obj_type)) if is_generic_type(t) else False:
            eltype_1: Any = get_generics(t)[0]
            match_value: Optional[Any] = o
            if match_value is not None:
                t_mut = eltype_1
                o_mut = value_30(match_value)
                continue

            else: 
                return Json(4)


        elif equals(get_generic_type_definition(t), list_type(obj_type)) if is_generic_type(t) else False:
            eltype_2: Any = get_generics(t)[0]
            def mapping_16(it_16: Any=None, t: Any=t, o: Any=o) -> Json:
                return obj_to_json(eltype_2, it_16)

            return Json(5, list(map_1(mapping_16, o)))

        elif is_record(t):
            def mapping_17(f: Any, t: Any=t, o: Any=o) -> Tuple[str, Json]:
                return (name(f), obj_to_json(f[1], get_record_field(o, f)))

            return Json(6, list(map(mapping_17, get_record_elements(t), None)))

        elif is_tuple(t):
            eltypes: Array[Any] = get_tuple_elements(t)
            def mapping_18(i_1: int, e: Any=None, t: Any=t, o: Any=o) -> Json:
                return obj_to_json(eltypes[i_1], e)

            return Json(5, list(map_indexed(mapping_18, get_tuple_fields(o), None)))

        elif is_union(t):
            pattern_input: Tuple[Any, Array[Any]] = get_union_fields(o, t)
            case: Any = pattern_input[0]
            def mapping_19(f_1: Any, t: Any=t, o: Any=o) -> Any:
                return f_1[1]

            fieldtypes: Array[Any] = map(mapping_19, get_union_case_fields(case), None)
            def mapping_20(i_2: int, e_1: Any=None, t: Any=t, o: Any=o) -> Json:
                return obj_to_json(fieldtypes[i_2], e_1)

            return Json(6, list(to_enumerable([(ADT_TAG, Json(3, name(case))), (ADT_VALS, Json(5, list(map_indexed(mapping_20, pattern_input[1], None))))])))

        else: 
            raise Exception(("unsupported data type fromJson: " + str(t)) + "")

        break


def escape_string(s: str) -> str:
    buf: Any = StringBuilder__ctor_Z524259A4(len(s))
    def rep(c: str, s: str=s) -> Any:
        if c == "\b":
            return StringBuilder__Append_Z721C83C5(buf, "\\b")

        elif c == "\t":
            return StringBuilder__Append_Z721C83C5(buf, "\\t")

        elif c == "\n":
            return StringBuilder__Append_Z721C83C5(buf, "\\n")

        elif c == "\f":
            return StringBuilder__Append_Z721C83C5(buf, "\\f")

        elif c == "\r":
            return StringBuilder__Append_Z721C83C5(buf, "\\r")

        elif c == "\"":
            return StringBuilder__Append_Z721C83C5(buf, "\\\"")

        elif c == "\\":
            return StringBuilder__Append_Z721C83C5(buf, "\\\\")

        else: 
            return StringBuilder__Append_244C7CD6(buf, c)


    for i in range(0, (len(s) - 1) + 1, 1):
        ignore(rep(s[i]))
    return to_string(buf)


def serialize_json(x: Json) -> str:
    if x.tag == 1:
        return to_string(x.fields[0])

    elif x.tag == 2:
        if x.fields[0]:
            return "true"

        else: 
            return "false"


    elif x.tag == 3:
        return ("\"" + escape_string(x.fields[0])) + "\""

    elif x.tag == 4:
        return "null"

    elif x.tag == 5:
        def _arrow45(x_1: Json, x: Json=x) -> str:
            return serialize_json(x_1)

        return ("[" + join(",", map_2(_arrow45, x.fields[0]))) + "]"

    elif x.tag == 6:
        def _arrow46(tupled_arg: Tuple[str, Json], x: Json=x) -> str:
            return ((("\"" + escape_string(tupled_arg[0])) + "\"") + ":") + serialize_json(tupled_arg[1])

        return ("{" + join(",", map_2(_arrow46, x.fields[0]))) + "}"

    else: 
        return int64_to_string(x.fields[0])



__all__ = ["Json_reflection", "Json__get_kind", "Parsec_pChar_", "Parsec_pStr_", "Parsec_pChar", "Parsec_pCharset_", "Parsec_pCharset", "Parsec_pIgnore", "Parsec_pSeq_", "Parsec_pSepRep", "Parsec_pSpc", "Parsec_allowSPC", "Parsec_la1", "Parsec_pNumber", "Parsec_pStr", "Parsec_pMap", "Parsec_pRef", "Parsec_Json_pListSep", "Parsec_Json_pDictSep", "Parsec_Json_jInt", "Parsec_Json_jFloat", "Parsec_Json_jNumber", "Parsec_Json_jTrue", "Parsec_Json_jFalse", "Parsec_Json_jNull", "Parsec_Json_jStr", "Parsec_Json_refObject", "Parsec_Json_jObject", "Parsec_Json_refList", "Parsec_Json_jList", "Parsec_Json_json", "parse_json", "int64from_json", "double_from_json", "bool_from_json", "string_from_json", "char_from_json", "unit_from_json", "ADT_TAG", "ADT_VALS", "evidence_1_reflection", "obj_from_json", "obj_to_json", "escape_string", "serialize_json"]

