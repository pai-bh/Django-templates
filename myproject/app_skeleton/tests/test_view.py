# test_view.py
import pytest
from rest_framework.test import APIClient
from datetime import datetime
import pytz
from apps.new_app.domain import ExampleDomain
from apps.new_app.dto import ExampleDomainDTO


@pytest.mark.django_db
def test_example_view_post():
    client = APIClient()
    # Given
    example_domain = ExampleDomain(
        id=1,
        name='Test Name',
        description='Test Description',
        created_at=datetime(2023, 6, 10, tzinfo=pytz.UTC),
        is_deleted=False
    )
    data = ExampleDomainDTO.from_domain(example_domain).dict()

    # When
    response = client.post('/new_app/example/', data, format='json')

    # Then
    assert response.status_code == 201
    response_data = response.json()
    assert response_data['id'] == data['id']
    assert response_data['name'] == data['name']
    assert response_data['description'] == data['description']
    # assert response_data['created_at'] == data['created_at']
    assert response_data['is_deleted'] == data['is_deleted']
