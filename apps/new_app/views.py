from rest_framework.decorators import api_view
from rest_framework import serializers
from drf_spectacular.utils import extend_schema, OpenApiResponse, extend_schema_view, inline_serializer
from django.shortcuts import render

from apps.new_app import services
from common import log_setter
from common.utils.swagger import generate_openapi_schema, generate_inline_serializer
from apps.new_app.dto import ExampleDomainDTO, ExampleCreateDTO

logger = log_setter.getLogger("appname")


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
    logger.info(f"example_view called with method {request.method}")
    if request.method == 'GET':
        response = services.example_view_get(request)
    elif request.method == 'POST':
        response = services.example_view_post(request)
    else:
        logger.error(f"Unsupported method: {request.method}")
        raise Exception("Not supported method")
    logger.info(f"example_view completed with status {response.status_code}")
    return response


@extend_schema_view(
    get=extend_schema(
        summary="Example API",
        description="An example API endpoint.",
        responses={200: OpenApiResponse(response=generate_openapi_schema(ExampleDomainDTO))}
    )
)
@api_view(['GET'])
def example_template_view(request, model_id):
    logger.info(f"example_template_view called with pk {model_id}")
    response = render(request, 'new_app/example.html', {'app_name': 'app_name', 'model_id': model_id})
    logger.info(f"example_template_view completed with status {response.status_code}")
    return response
