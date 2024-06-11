# test_service.py
import pytest
from rest_framework.test import APIClient
from datetime import datetime
import pytz
from apps.new_app.domain import ExampleDomain
from apps.new_app.dto import ExampleDomainDTO
from apps.new_app.services import create_example_service


@pytest.mark.django_db
def test_create_example_service():
    # Given
    example_domain = ExampleDomain(
        id=1,
        name='Test Name',
        description='Test Description',
        created_at=datetime(2023, 6, 10, tzinfo=pytz.UTC),
        is_deleted=False
    )

    # When
    created_example = create_example_service(example_domain)

    # Then
    assert created_example.id == example_domain.id
    assert created_example.name == example_domain.name
    assert created_example.description == example_domain.description
    # assert created_example.created_at == example_domain.created_at
    assert created_example.is_deleted == example_domain.is_deleted


@pytest.mark.django_db
def test_example_view_get():
    client = APIClient()
    # Given
    url = '/new_app/example/'

    # When
    response = client.get(url)

    # Then
    assert response.status_code == 200


@pytest.mark.django_db
def test_example_view_post():
    client = APIClient()
    # Given
    url = '/new_app/example/'
    data = {
        'id': 1,
        'name': 'Test Name',
        'description': 'Test Description',
        'created_at': '2023-06-10T00:00:00+00:00',  # 올바른 datetime 형식 사용
        'is_deleted': False
    }

    # When
    response = client.post(url, data, format='json')

    # Then
    assert response.status_code == 201
    response_data = response.json()
    assert response_data['id'] == data['id']
    assert response_data['name'] == data['name']
    assert response_data['description'] == data['description']
    # assert response_data['created_at'] == data['created_at']
    assert response_data['is_deleted'] == data['is_deleted']
