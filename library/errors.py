"""Класи винятків домену 'Бібліотека'."""

from __future__ import annotations


class LibraryError(Exception):
    """Базовий клас усіх винятків цього домену."""


class BookNotFound(LibraryError):
    """Піднімається, коли книгу з даним ISBN не знайдено в каталозі."""

    def __init__(self, isbn: str) -> None:
        super().__init__(f"Книгу з ISBN {isbn!r} не знайдено в каталозі")
        self.isbn = isbn
