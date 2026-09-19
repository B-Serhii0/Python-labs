"""Завдання 6"""
from typing import Iterable, Iterator

from .pipeline import parse, normalize, keep, DEFAULT_THRESHOLD


# 6.1 Конвеєр на генераторах

def g_parse(lines: Iterable[str]) -> Iterator[dict]:
    """Ледачий розбір"""
    for line in lines:
        rec = parse(line)
        if rec is not None:
            yield rec


def g_normalize(records: Iterable[dict]) -> Iterator[dict]:
    for rec in records:
        yield normalize(rec)


def g_keep(records: Iterable[dict], threshold: int = DEFAULT_THRESHOLD) -> Iterator[dict]:
    for rec in records:
        if keep(rec, threshold):
            yield rec


def lazy_pipeline(lines: Iterable[str], threshold: int = DEFAULT_THRESHOLD) -> Iterator[dict]:
    """Ланцюжок генераторів"""
    return g_keep(g_normalize(g_parse(lines)), threshold)


# 6.2 Нескінченний потік

def record_stream() -> Iterator[dict]:
    """Нескінченні списки"""
    methods = ["get", "post", "put", "delete"]
    i = 0
    while True:
        yield {
            "method": methods[i % len(methods)],
            "path": f"/api/resource{i % 7}",
            "status": "200",
            "bytes": str((i * 37) % 100),
        }
        i += 1


# 6.3 Власні генератори (без itertools)

def take(n: int, it: Iterable):
    """N ітератори"""
    it = iter(it)
    count = 0
    for item in it:
        if count >= n:
            return
        yield item
        count += 1


def drop(n: int, it: Iterable):
    """Ітератори"""
    it = iter(it)
    count = 0
    for item in it:
        if count < n:
            count += 1
            continue
        yield item
