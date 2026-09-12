"""Колекція сутностей (завдання 3, 4).

Catalog — контейнер книг, що надає операції доступу, обходу й запиту.
"""

from __future__ import annotations

from typing import Iterable, Iterator, List, Optional

from .decorators import validated
from .entities import Book
from .errors import BookNotFound


class _PageIterator:
    """Об'єкт-ітератор посторінкового обходу каталогу (завдання 3.2).

    Тримає посилання на той самий екземпляр Catalog (елементи не
    копіюються) і поточний індекс; звертається до __len__/__getitem__
    самого каталогу.
    """

    def __init__(self, catalog: "Catalog", page_size: int) -> None:
        if page_size <= 0:
            raise ValueError("page_size: розмір сторінки повинен бути додатним")
        self._catalog = catalog
        self._page_size = page_size
        self._index = 0

    def __iter__(self) -> "_PageIterator":
        return self

    def __next__(self) -> List[Book]:
        if self._index >= len(self._catalog):
            raise StopIteration
        end = min(self._index + self._page_size, len(self._catalog))
        page = [self._catalog[i] for i in range(self._index, end)]
        self._index = end
        return page


class Catalog:
    __slots__ = ("_books",)

    _ALLOWED_QUERIES = {"author", "year_from", "year_to"}

    def __init__(self, books: Optional[Iterable[Book]] = None) -> None:
        self._books: List[Book] = list(books) if books is not None else []

    # --- протокол послідовності (3.1) ---
    def __len__(self) -> int:
        return len(self._books)

    def __getitem__(self, index):
        if isinstance(index, slice):
            return Catalog(self._books[index])
        return self._books[index]

    def __contains__(self, item) -> bool:
        isbn = item.isbn if isinstance(item, Book) else item
        return any(b.isbn == isbn for b in self._books)

    def __iter__(self) -> Iterator[Book]:
        return iter(self._books)

    # --- посторінковий обхід (3.2) ---
    def pages(self, page_size: int) -> _PageIterator:
        return _PageIterator(self, page_size)

    # --- запит як виклик (3.3) ---
    def __call__(self, **criteria) -> "Catalog":
        unknown = set(criteria) - self._ALLOWED_QUERIES
        if unknown:
            raise TypeError(
                f"невідомі критерії запиту: {sorted(unknown)}; "
                f"припустимі: {sorted(self._ALLOWED_QUERIES)}"
            )

        result = list(self._books)
        if "author" in criteria:
            author = criteria["author"]
            result = [b for b in result if b.author == author]
        if "year_from" in criteria:
            year_from = criteria["year_from"]
            result = [b for b in result if b.year >= year_from]
        if "year_to" in criteria:
            year_to = criteria["year_to"]
            result = [b for b in result if b.year <= year_to]
        return Catalog(result)

    # --- пошук за ідентифікатором, стиль EAFP (3.4) ---
    def get(self, isbn: str) -> Book:
        index = {b.isbn: b for b in self._books}
        try:
            return index[isbn]
        except KeyError:
            raise BookNotFound(isbn) from None

    # --- перевантаження операторів (4.1) ---
    def __add__(self, other: "Catalog") -> "Catalog":
        if not isinstance(other, Catalog):
            return NotImplemented
        merged = {b.isbn: b for b in self._books}
        for b in other._books:
            merged.setdefault(b.isbn, b)
        return Catalog(list(merged.values()))

    def __radd__(self, other):
        # Потрібен для sum([cat_a, cat_b, cat_c]): sum починає з 0.
        if other == 0:
            return Catalog(list(self._books))
        return self.__add__(other)

    # --- методи, до яких застосовано валідаційний декоратор (завдання 5) ---
    @validated(title="non_empty", author="non_empty", copies="positive")
    def add_book_copies(self, *, isbn: str, title: str, author: str, year: int, copies: int) -> None:
        """Додає нову книгу до каталогу (демонстрація декоратора validated)."""
        self._books.append(Book(isbn=isbn, title=title, author=author, year=year, copies=copies))

    @validated(title="non_empty")
    def rename_book(self, *, isbn: str, title: str) -> None:
        """Перейменовує наявну книгу за ISBN (другий метод із декоратором)."""
        book = self.get(isbn)
        book.title = title

    def __repr__(self) -> str:
        return f"Catalog({self._books!r})"
