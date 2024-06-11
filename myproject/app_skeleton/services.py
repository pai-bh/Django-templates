from rest_framework.response import Response
from django.shortcuts import render
from apps.appname.dto import ExampleDomainDTO
from apps.appname.repository import ExampleDomainRepository
from apps.appname.domain import ExampleDomain


def example_view_get(request):
    return render(request, 'new_app/example.html')


def example_view_post(request):
    data = ExampleDomainDTO(**request.data)
    created_example = create_example_service(data.to_domain())
    return Response(ExampleDomainDTO.from_domain(created_example).dict(), status=201)


def create_example_service(data: ExampleDomain) -> ExampleDomain:
    repository = ExampleDomainRepository()
    created_example = repository.create(data)
    return created_example
