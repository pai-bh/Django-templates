from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ExampleDomain:
    id: Optional[int]
    name: str
    description: Optional[str]
    created_at: datetime
    is_deleted: bool

    @staticmethod
    def new(id: Optional[int], name: str, description: Optional[str], created_at: datetime,
            is_deleted: bool = False) -> 'ExampleDomain':
        return ExampleDomain(id, name, description, created_at, is_deleted)
