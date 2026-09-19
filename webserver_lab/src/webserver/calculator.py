"""Завдання 7"""
from dataclasses import dataclass
from typing import Union


@dataclass(frozen=True)
class Num:
    value: float


@dataclass(frozen=True)
class Neg:
    x: "Expr"


@dataclass(frozen=True)
class Add:
    a: "Expr"
    b: "Expr"


@dataclass(frozen=True)
class Sub:
    a: "Expr"
    b: "Expr"


@dataclass(frozen=True)
class Mul:
    a: "Expr"
    b: "Expr"


@dataclass(frozen=True)
class Div:
    a: "Expr"
    b: "Expr"


@dataclass(frozen=True)
class Pow:
    base: "Expr"
    exp: int


@dataclass(frozen=True)
class Sqrt:
    x: "Expr"


@dataclass(frozen=True)
class Sum:
    terms: tuple


Expr = Union[Num, Neg, Add, Sub, Mul, Div, Pow, Sqrt, Sum]


def evaluate(node: Expr) -> float:
    """Обчислює вираз"""
    match node:
        case Num(0):
            return 0.0
        case Num(v):
            return float(v)
        case Neg(x):
            return -evaluate(x)
        case Add(a, b):
            return evaluate(a) + evaluate(b)
        case Sub(a, b):
            return evaluate(a) - evaluate(b)
        case Mul(a, b):
            return evaluate(a) * evaluate(b)
        case Div(a, b):
            bv = evaluate(b)
            if bv == 0:
                raise ValueError("ділення на нуль")
            return evaluate(a) / bv
        case Pow(base, exp) if exp >= 0:
            return evaluate(base) ** exp
        case Pow(_, _):
            raise ValueError("від'ємний показник")
        case Sqrt(x):
            xv = evaluate(x)
            if xv < 0:
                raise ValueError("корінь із від'ємного числа")
            return xv ** 0.5
        case Sum(()):
            return 0.0
        case Sum((head, *rest)):
            return evaluate(head) + evaluate(Sum(tuple(rest)))
        case _:
            raise ValueError(f"невідомий вузол: {node!r}")
