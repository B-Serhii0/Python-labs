"""Доменна сутність (завдання 2).

Book — основний об'єкт домену: має ідентифікатор (ISBN) і поля, коректність
яких контролюється через property-гетери/сетери.
"""

from __future__ import annotations

import datetime
import re

from .values import MIN_YEAR

_ISBN_RE = re.compile(r"^\d{9}[\dXx]$|^\d{13}$")


class Book:
    __slots__ = ("_isbn", "_title", "_author", "_year", "_copies")

    def __init__(self, isbn: str, title: str, author: str, year: int, copies: int) -> None:
        # Конструктор присвоює поля через ті самі сетери, що й зовнішній код (2.1).
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year
        self.copies = copies

    # --- isbn (ідентифікатор) ---
    @property
    def isbn(self) -> str:
        return self._isbn

    @isbn.setter
    def isbn(self, value: str) -> None:
        if not Book.is_valid_isbn(value):
            raise ValueError(f"isbn: некоректний формат ISBN {value!r}")
        self._isbn = value.replace("-", "").replace(" ", "")

    # --- title ---
    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("title: назва книги не може бути порожньою")
        self._title = value

    # --- author ---
    @property
    def author(self) -> str:
        return self._author

    @author.setter
    def author(self, value: str) -> None:
        if not isinstance(value, str) or not value.strip():
            raise ValueError("author: ім'я автора не може бути порожнім")
        self._author = value

    # --- year ---
    @property
    def year(self) -> int:
        return self._year

    @year.setter
    def year(self, value: int) -> None:
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError("year: рік видання повинен бути цілим числом")
        current_year = datetime.date.today().year
        if not (MIN_YEAR <= value <= current_year):
            raise ValueError(
                f"year: рік видання повинен бути у діапазоні {MIN_YEAR}..{current_year}"
            )
        self._year = value

    # --- copies ---
    @property
    def copies(self) -> int:
        return self._copies

    @copies.setter
    def copies(self, value: int) -> None:
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError("copies: кількість примірників не може бути від'ємною")
        self._copies = value

    # --- метод класу та статичний метод (2.2) ---
    @classmethod
    def from_dict(cls, data: dict) -> "Book":
        """Створює Book зі словника 'сирих' значень із тими самими перевірками."""
        return cls(
            isbn=data["isbn"],
            title=data["title"],
            author=data["author"],
            year=data["year"],
            copies=data["copies"],
        )

    @staticmethod
    def is_valid_isbn(value: str) -> bool:
        """Перевіряє формат ISBN-10 або ISBN-13 (без звернення до self/cls)."""
        if not isinstance(value, str):
            return False
        cleaned = value.replace("-", "").replace(" ", "")
        return bool(_ISBN_RE.match(cleaned))

    def __repr__(self) -> str:
        return (
            f"Book(isbn={self._isbn!r}, title={self._title!r}, "
            f"author={self._author!r}, year={self._year}, copies={self._copies})"
        )

    def __str__(self) -> str:
        return f'"{self._title}" ({self._author}, {self._year})'
