from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from apps.appname.domain import ExampleDomain


class OkDTO(BaseModel):
    ok: bool


class ExampleDomainDTO(BaseModel):
    id: Optional[int] = Field(default=None, description="ID", example=["example_id"])
    name: str = Field(description="Name", example=["example_name"])
    description: Optional[str] = Field(default=None, description="Description", examples=[["LLM", "LangChain"]])
    created_at: datetime = Field(description="Creation Date", examples=["2024-06-03T00:00:00+00:00"])
    is_deleted: bool

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat(),
        }

    def to_domain(self):
        return ExampleDomain.new(
            id=self.id,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            is_deleted=self.is_deleted
        )

    @staticmethod
    def from_domain(domain: ExampleDomain):
        return ExampleDomainDTO(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            created_at=domain.created_at,
            is_deleted=domain.is_deleted
        )


class ExampleCreateDTO(BaseModel):
    name: str = Field(description="Name", examples=["Example Name"])
    description: Optional[str] = Field(description="Description", examples=["This is an example."])
    created_at: datetime = Field(description="Creation Date", examples=["2024-06-03T00:00:00+00:00"])

    def to_domain(self):
        return ExampleDomain.new(
            id=None,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            is_deleted=False
        )
