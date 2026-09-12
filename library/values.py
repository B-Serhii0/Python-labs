"""Об'єкт-значення предметної області (завдання 1, 4).

Year — рік видання книги: невеликий незмінний тип, що порівнюється за
вмістом (значенням поля), а не за ідентичністю посилання.
"""

from __future__ import annotations

import datetime
import functools
from dataclasses import dataclass

MIN_YEAR = 1450
CURRENT_YEAR = datetime.date.today().year


@functools.total_ordering
class Year:
    """Незмінний об'єкт-значення 'рік' (ручна реалізація, завдання 1.1-1.5)."""

    __slots__ = ("value", "_frozen")

    def __init__(self, value: int) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("value: рік повинен бути цілим числом")
        object.__setattr__(self, "value", value)
        object.__setattr__(self, "_frozen", True)

    def __setattr__(self, name, value) -> None:
        if getattr(self, "_frozen", False):
            raise AttributeError("об'єкт Year незмінний")
        object.__setattr__(self, name, value)

    # --- рядкові подання (1.3) ---
    def __repr__(self) -> str:
        return f"Year(value={self.value})"

    def __str__(self) -> str:
        return f"{self.value} р."

    # --- порівняння та впорядкування (1.4) ---
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Year):
            return NotImplemented
        return self.value == other.value

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Year):
            return NotImplemented
        return self.value < other.value

    # --- хешованість (1.5) ---
    def __hash__(self) -> int:
        return hash(self.value)

    # --- арифметика (завдання 4.2) ---
    def __add__(self, other: "Year") -> "Year":
        if not isinstance(other, Year):
            return NotImplemented
        return Year(self.value + other.value)

    def __sub__(self, other: "Year") -> "Year":
        if not isinstance(other, Year):
            return NotImplemented
        return Year(self.value - other.value)

    def __mul__(self, factor: float) -> "Year":
        if not isinstance(factor, (int, float)) or isinstance(factor, bool):
            return NotImplemented
        return Year(round(self.value * factor))

    def __rmul__(self, factor: float) -> "Year":
        return self.__mul__(factor)


@dataclass(frozen=True, slots=True, order=True)
class YearDC:
    """Альтернативна реалізація Year (завдання 1.2): @dataclass(frozen=True, slots=True).

    dataclass із frozen=True сам генерує __init__, __repr__, __eq__ і (за
    order=True) операції порівняння; slots=True забороняє додавання нових
    атрибутів так само, як явний __slots__ у Year.
    """

    value: int

    def __str__(self) -> str:
        return f"{self.value} р."
