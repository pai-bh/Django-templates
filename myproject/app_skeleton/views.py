from rest_framework.decorators import api_view
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view, inline_serializer
from django.shortcuts import render

from common.utils.swagger import generate_openapi_schema, generate_inline_serializer
from apps.appname import services
from apps.appname.dto import ExampleDomainDTO, ExampleCreateDTO

@extend_schema_view(
    get=extend_schema(
        summary="Example API GET",
        description="An example API endpoint for GET request.",
        responses={200: OpenApiResponse(response=generate_openapi_schema(ExampleDomainDTO))}
    ),
    post=extend_schema(
        summary="Example API POST",
        description="An example API endpoint for POST request.",
        request=generate_inline_serializer(ExampleCreateDTO),
        responses={201: OpenApiResponse(response=generate_openapi_schema(ExampleDomainDTO))}
    )
)
@api_view(['GET', 'POST'])
def example_view(request):
    if request.method == 'GET':
        return services.example_view_get(request)
    elif request.method == 'POST':
        return services.example_view_post(request)
    else:
        raise Exception("Not supported method")


@extend_schema_view(
    get=extend_schema(
        summary="Example API",
        description="An example API endpoint.",
        responses={200: OpenApiResponse(response=generate_openapi_schema(ExampleDomainDTO))}
    )
)
@api_view(['GET'])
def example_template_view(request, pk):
    return render(request, 'new_app/example.html', {'app_name': 'app_name', 'pk': pk})
