from django.db import models
from apps.new_app.domain import ExampleDomain


class ExampleDomainModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_deleted = models.BooleanField(default=False)

    def to_domain(self):
        return ExampleDomain(
            id=self.id,
            name=self.name,
            description=self.description,
            created_at=self.created_at,
            is_deleted=self.is_deleted
        )

    @staticmethod
    def from_domain(domain):
        return ExampleDomainModel(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            created_at=domain.created_at,
            is_deleted=False
        )

    class Meta:
        db_table = 'example_domain_tb'
