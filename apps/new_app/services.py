import logging
from rest_framework.response import Response
from django.shortcuts import render

from common import log_setter
from .dto import ExampleDomainDTO, ExampleCreateDTO
from .repository import ExampleDomainRepository
from .domain import ExampleDomain

logger = log_setter.getLogger("appname")
"""publcai BH : 서비스 함수에서는 DEBUG 로그를 권장합니다."""


def example_view_get(request):
    logger.debug("example_view_get called")
    example_data = {
        'id': 1,
        'name': 'Example Name',
        'description': 'This is an example description.',
        'created_at': '2024-06-03T00:00:00+00:00',
        'is_deleted': False,
    }
    return render(request, 'new_app/example.html', {'example_data': example_data})


def example_view_post(request):
    logger.debug("example_view_post called")
    try:
        data = ExampleCreateDTO(
            name=request.POST['name'],
            description=request.POST.get('description', None),
            created_at=request.POST['created_at']
        )
        created_example = create_example_service(data.to_domain())
        logger.debug(f"Created example with id {created_example.id}")
        return Response(ExampleDomainDTO.from_domain(created_example).dict(), status=201)
    except Exception as e:
        logger.error(f"Error in example_view_post: {str(e)}")
        return Response({'error': str(e)}, status=500)


def create_example_service(data: ExampleDomain) -> ExampleDomain:
    logger.debug("create_example_service called with data: %s", data)
    repository = ExampleDomainRepository()
    created_example = repository.create(data)
    logger.debug("Example created with id: %s", created_example.id)
    return created_example
