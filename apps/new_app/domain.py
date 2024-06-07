from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ExampleDomain:
    id: Optional[int]
    name: str
    description: Optional[str]
    created_at: datetime

    @staticmethod
    def new(id: Optional[int], name: str, description: Optional[str], created_at: datetime) -> 'ExampleDomain':
        return ExampleDomain(id, name, description, created_at)
