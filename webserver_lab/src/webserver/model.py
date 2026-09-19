"""Завдання 2"""
from dataclasses import dataclass, replace


@dataclass(frozen=True, slots=True)
class Record:
    """Незмінний запис."""
    method: str
    path: str
    status: int
    bytes: int
    received_at: float


def to_record(d: dict) -> Record:
    """2.1"""
    return Record(
        method=d["method"],
        path=d["path"],
        status=d["status"],
        bytes=d["bytes"],
        received_at=d["received_at"],
    )


def bump_bytes(rec: Record, delta: int) -> Record:
    """2.2"""
    return replace(rec, bytes=rec.bytes + delta)


def rename_path(rec: Record, new_path: str) -> Record:
    """2.2"""
    return replace(rec, path=new_path)
