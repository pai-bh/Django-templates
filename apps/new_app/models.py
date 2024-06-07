from django.db import models


class ExampleDomainModel(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def to_domain(self):
        from domain import ExampleDomain
        return ExampleDomain(
            id=self.id,
            name=self.name,
            description=self.description,
            created_at=self.created_at
        )

    @staticmethod
    def from_domain(domain):
        return ExampleDomainModel(
            id=domain.id,
            name=domain.name,
            description=domain.description,
            created_at=domain.created_at
        )
