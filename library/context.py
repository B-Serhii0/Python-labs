"""Контекстний менеджер пакетних змін (завдання 6)."""

from __future__ import annotations

import copy
from types import TracebackType
from typing import Optional, Type


class AcquisitionSession:
    """Сеанс пакетного поповнення каталогу.

    Усі зміни, внесені у блоці `with`, застосовуються разом лише за
    відсутності винятку; інакше каталог повертається до стану на момент
    входу в сеанс.
    """

    def __init__(self, catalog) -> None:
        self._catalog = catalog
        self._snapshot = None

    def __enter__(self):
        self._snapshot = copy.deepcopy(self._catalog)
        return self._catalog

    def __exit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc: Optional[BaseException],
        tb: Optional[TracebackType],
    ) -> bool:
        if exc_type is not None:
            # Відкат: повертаємо список книг каталогу до знімка на вході.
            self._catalog._books[:] = self._snapshot._books
        return False  # виняток не приховується
