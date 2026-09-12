"""Пакет 'library' — предметна область 'Бібліотека' (варіант 1).

Реекспортує публічні класи так, щоб клієнтський код міг писати:
    from library import Year, Book, Catalog, ...
"""

from .values import Year, YearDC
from .entities import Book
from .collections_ import Catalog
from .decorators import validated
from .context import AcquisitionSession
from .errors import LibraryError, BookNotFound

__all__ = [
    "Year",
    "YearDC",
    "Book",
    "Catalog",
    "validated",
    "AcquisitionSession",
    "LibraryError",
    "BookNotFound",
]
