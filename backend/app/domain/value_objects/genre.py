from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Genre:
    name: str

    def __post_init__(self) -> None:
        object.__setattr__(self, "name", self.name.strip().title())

    def __str__(self) -> str:
        return self.name
