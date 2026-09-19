"""Завдання 3 Завдання 5"""
import operator
from functools import partial
from typing import Callable


# 3.1 Композиція

def compose2(f: Callable, g: Callable) -> Callable:
    """Повертає функцію x"""
    return lambda x: f(g(x))


def compose(*funcs: Callable) -> Callable:
    """Застосування справа наліво"""
    def composed(x):
        result = x
        for f in reversed(funcs):
            result = f(result)
        return result
    return composed


def pipe(*funcs: Callable) -> Callable:
    """Застосування зліва направо"""
    def piped(x):
        result = x
        for f in funcs:
            result = f(result)
        return result
    return piped


#перетворення

def strip_strings(rec: dict) -> dict:
    return {**rec, "method": rec["method"].strip(), "path": rec["path"].strip()}


def lower_category(rec: dict) -> dict:
    return {**rec, "path": rec["path"].lower()}


def to_int_number(rec: dict) -> dict:
    return {**rec, "status": int(rec["status"]), "bytes": int(rec["bytes"])}


# 3.1: normalize
normalize_pipe = pipe(strip_strings, lower_category, to_int_number)

# 3.2: список
ELEMENTARY_STEPS = [strip_strings, lower_category, to_int_number]


def normalize_via_loop(rec: dict) -> dict:
    """3.2"""
    result = rec
    for step in ELEMENTARY_STEPS:
        result = step(result)
    return result


# 3.3 Замикання

def make_predicate(field: str, op: str, value) -> Callable[[dict], bool]:
    """Повертає предикат rec -> bool"""
    binop = getattr(operator, op)

    def predicate(rec: dict) -> bool:
        return binop(rec[field], value)
    return predicate


def make_running_total() -> Callable[[float], float]:
    """Повертає функцію-акумулятор із власним станом (через nonlocal)"""
    total = 0

    def add(x):
        nonlocal total
        total += x
        return total
    return add


def classify_bytes(rec: dict, field: str = "bytes") -> str:
    """3.4: лямбда"""
    classifier = lambda v: "мало" if v < 5 else ("звичайно" if v < 20 else "багато")
    return classifier(rec[field])


# 5.1 functools.partial

def scale(factor: float, value: float) -> float:
    """Двоаргументна функція множення з округленням."""
    return round(factor * value, 3)


to_km = partial(scale, 1.609)          # милі -> км
to_miles = partial(scale, 1 / 1.609)   # км -> милі


def make_keep_partial(field: str = "bytes", op: str = "ge"):
    """5.1"""
    return partial(make_predicate, field, op)


# 5.2 Каррирування

def curry3(f: Callable) -> Callable:
    """curry3(f)(a)(b)(c) == f(a, b, c)"""
    def with_a(a):
        def with_b(b):
            def with_c(c):
                return f(a, b, c)
            return with_c
        return with_b
    return with_a


curried_predicate = curry3(make_predicate)
