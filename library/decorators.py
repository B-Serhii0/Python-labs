"""Валідаційний декоратор з параметрами (завдання 5)."""

from __future__ import annotations

import functools
from typing import Callable


def validated(**rules: str) -> Callable:
    """Декоратор-фабрика: перевіряє іменовані аргументи методу перед викликом.

    Підтримувані правила:
      - "positive"     — число строго більше за нуль;
      - "non_empty"    — рядок, що після str.strip() не порожній;
      - "one_of:a,b,c" — значення належить переліченій множині.

    Складається з трьох рівнів вкладених функцій: validated (приймає
    параметри правил) -> decorator (приймає функцію, що декорується) ->
    wrapper (виконується замість неї).
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for name, rule in rules.items():
                if name not in kwargs:
                    continue
                value = kwargs[name]

                if rule == "positive":
                    if not isinstance(value, (int, float)) or isinstance(value, bool) or value <= 0:
                        raise ValueError(f"{name}: значення повинне бути додатним числом")

                elif rule == "non_empty":
                    if not isinstance(value, str) or not value.strip():
                        raise ValueError(f"{name}: рядок не може бути порожнім")

                elif rule.startswith("one_of:"):
                    allowed = rule[len("one_of:"):].split(",")
                    if value not in allowed:
                        raise ValueError(f"{name}: значення повинне бути одним із {allowed}")

                else:
                    raise ValueError(f"невідоме правило валідації: {rule!r}")

            return func(*args, **kwargs)

        return wrapper

    return decorator
