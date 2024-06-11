from typing import List, Optional
from django.db import transaction
from apps.new_app.models import ExampleDomainModel
from common.exceptions import NotFoundException
from .domain import ExampleDomain
# from apps.new_app.exceptions import NotFoundException
# from apps.new_app.models import ExampleDomainModel
# from apps.new_app.domain import ExampleDomain
from django.core.exceptions import ObjectDoesNotExist


class ExampleDomainRepository:

    @staticmethod
    @transaction.atomic
    def create(domain: ExampleDomain) -> ExampleDomain:
        entity = ExampleDomainModel.from_domain(domain)
        entity.save()
        return entity.to_domain()

    @staticmethod
    @transaction.atomic
    def update(domain: ExampleDomain) -> ExampleDomain:
        try:
            entity = ExampleDomainModel.objects.get(id=domain.id)
            entity.name = domain.name
            entity.description = domain.description
            entity.created_at = domain.created_at
            entity.save()
            return entity.to_domain()
        except ObjectDoesNotExist:
            raise NotFoundException(f"ExampleDomain with id {domain.id} not found")

    @staticmethod
    @transaction.atomic
    def delete(domain_id: int) -> None:
        try:
            entity = ExampleDomainModel.objects.get(id=domain_id)
            entity.delete()
        except ObjectDoesNotExist:
            raise NotFoundException(f"ExampleDomain with id {domain_id} not found")

    @staticmethod
    def get_by_id(domain_id: int) -> Optional[ExampleDomain]:
        try:
            entity = ExampleDomainModel.objects.get(id=domain_id)
            return entity.to_domain()
        except ObjectDoesNotExist:
            raise NotFoundException(f"ExampleDomain with id {domain_id} not found")

    @staticmethod
    def find_all() -> List[ExampleDomain]:
        entities = ExampleDomainModel.objects.all()
        return [entity.to_domain() for entity in entities]

    @staticmethod
    def find_by(**kwargs) -> List[ExampleDomain]:
        entities = ExampleDomainModel.objects.filter(**kwargs)
        return [entity.to_domain() for entity in entities]
