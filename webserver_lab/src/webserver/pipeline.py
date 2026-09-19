"""Завдання 1 та 4

Формат запису варіанта 1: 'method;path;status;bytes'
- категорійне поле (групування, eq):  path
- числове поле (сума, ge-фільтр):     bytes
"""
from dataclasses import dataclass
from functools import reduce
from typing import Any, Dict, Iterable, Optional

CATEGORY_FIELD = "path"
NUMERIC_FIELD = "bytes"
DEFAULT_THRESHOLD = 5


def _is_int(s: str) -> bool:
    s = s.strip()
    if s.startswith("-"):
        s = s[1:]
    return s.isdigit() and s != ""


def parse(line: str) -> Optional[Dict[str, str]]:
    """Крок 1. Ділить рядок за ';'"""
    parts = line.split(";")
    if len(parts) != 4:
        return None
    method, path, status, nbytes = (p.strip() for p in parts)
    if not method or not path:
        return None
    if not _is_int(status) or not _is_int(nbytes):
        return None
    return {"method": method, "path": path, "status": status, "bytes": nbytes}


def normalize(rec: Dict[str, str]) -> Dict[str, Any]:
    """Крок 2. Рядкові поля -> strip; """
    return {
        "method": rec["method"].strip(),
        "path": rec["path"].strip().lower(),
        "status": int(rec["status"].strip()),
        "bytes": int(rec["bytes"].strip()),
    }


def keep(rec: dict, threshold: int = DEFAULT_THRESHOLD) -> bool:
    """Крок 3. Предикат відбору: числове поле >= порогу."""
    return rec[NUMERIC_FIELD] >= threshold


def add_to_groups(acc: dict, rec: dict) -> dict:
    """Акумулятор для reduce (крок 4): додає bytes запису до групи за path."""
    key = rec[CATEGORY_FIELD]
    acc[key] = acc.get(key, 0) + rec[NUMERIC_FIELD]
    return acc


def aggregate(records: Iterable[dict]) -> dict:
    """Крок 4. Групує записи за категорійним полем, підсумовує числове поле."""
    return reduce(add_to_groups, records, {})


@dataclass(frozen=True)
class Result:
    """1.1: результат чистої обробки"""
    records: tuple
    errors: int


def process(lines: Iterable[str], now: float) -> "Result":
    """1.1: чиста функція."""
    good = []
    errors = 0
    for line in lines:
        rec = parse(line)
        if rec is None:
            errors += 1
            continue
        rec = normalize(rec)
        rec = {**rec, "received_at": now}
        good.append(rec)
    return Result(records=tuple(good), errors=errors)


def pipeline(lines: Iterable[str], threshold: int = DEFAULT_THRESHOLD) -> Dict[str, int]:
    """4.1: спосіб A — map / filter / reduce."""
    parsed = (r for r in map(parse, lines) if r is not None)
    normalized = map(normalize, parsed)
    filtered = filter(lambda r: keep(r, threshold), normalized)
    return aggregate(filtered)


def pipeline_comprehension(lines: Iterable[str], threshold: int = DEFAULT_THRESHOLD) -> Dict[str, int]:
    """4.2: спосіб B — спискові включення + явний цикл для агрегації."""
    raw = [parse(line) for line in lines]
    normalized: list = [normalize(r) for r in raw if r is not None]
    filtered: list = [r for r in normalized if keep(r, threshold)]
    result: Dict[str, int] = {}
    for r in filtered:
        result[r[CATEGORY_FIELD]] = result.get(r[CATEGORY_FIELD], 0) + r[NUMERIC_FIELD]
    return result
