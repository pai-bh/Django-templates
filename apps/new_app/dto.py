from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .domain import ExampleDomain
# 권장사항을 아래와 같습니다.
# from apps.new_app.domain import ExampleDomain


class ExampleDomainDTO(BaseModel):
    id: Optional[int] = Field(default=None, description="ID")
    name: str = Field(description="Name")
    description: Optional[str] = Field(default=None, description="Description")
    created_at: datetime = Field(description="Creation Date")

    def to_domain(self):
        return ExampleDomain.new(
            id=self.id,
            name=self.name,
            description=self.description,
            created_at=self.created_at
        )

    @staticmethod
    def from_domain(domain: ExampleDomain):
        return ExampleDomainDTO(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            created_at=domain.created_at
        )
