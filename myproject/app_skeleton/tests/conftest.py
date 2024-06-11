import pytest
import os
import django
from django.conf import settings

from apps.new_app.services import create_example_service
from apps.new_app.repository import ExampleDomainRepository
from apps.new_app.domain import ExampleDomain


def pytest_configure():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
    if not settings.configured:
        settings.configure(
            INSTALLED_APPS=[
                'django.contrib.contenttypes',
                'django.contrib.auth',
                # ... 기타 필요한 기본 앱들 ...
                'apps.new_app',  # 테스트할 애플리케이션 추가
            ],
            DATABASES={
                'default': {
                    'ENGINE': 'django.db.backends.sqlite3',
                    'NAME': ':memory:',
                }
            },
        )
    django.setup()


@pytest.fixture
def example_domain():
    return ExampleDomain(id=1, name="Test Name", description="Test Description", created_at="2023-06-10",
                         is_deleted=False)


@pytest.fixture
def example_service():
    return create_example_service()


@pytest.fixture
def example_repository():
    return ExampleDomainRepository()
