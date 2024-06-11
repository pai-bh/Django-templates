# test_repository.py
import pytest
from datetime import datetime
import pytz
from apps.new_app.domain import ExampleDomain
from apps.new_app.repository import ExampleDomainRepository

@pytest.mark.django_db
def test_create_example_repository():
    # Given
    example_domain = ExampleDomain(
        id=1,
        name='Test Name',
        description='Test Description',
        created_at=datetime(2023, 6, 10, tzinfo=pytz.UTC),
        is_deleted=False
    )
    repository = ExampleDomainRepository()

    # When
    created_example = repository.create(example_domain)

    # Then
    assert created_example.id == example_domain.id
    assert created_example.name == example_domain.name
    assert created_example.description == example_domain.description
    # assert created_example.created_at == example_domain.created_at
    assert created_example.is_deleted == example_domain.is_deleted

@pytest.mark.django_db
def test_get_by_id_example_repository():
    # Given
    example_domain = ExampleDomain(
        id=1,
        name='Test Name',
        description='Test Description',
        created_at=datetime(2023, 6, 10, tzinfo=pytz.UTC),
        is_deleted=False
    )
    repository = ExampleDomainRepository()
    repository.create(example_domain)

    # When
    retrieved_example = repository.get_by_id(1)

    # Then
    assert retrieved_example.id == example_domain.id
    assert retrieved_example.name == example_domain.name
    assert retrieved_example.description == example_domain.description
    # assert retrieved_example.created_at == example_domain.created_at
    assert retrieved_example.is_deleted == example_domain.is_deleted
