"""Рекурсивний підсумок"""
from typing import Sequence


def total(records: Sequence[dict], field: str = "bytes") -> int:
    """Рекурсивно підсумовує поле `field` по послідовності записів."""
    if not records:
        return 0
    head, *tail = records
    return head[field] + total(tail, field)
