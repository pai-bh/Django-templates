from rest_framework.decorators import api_view
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import render

from apps.new_app import services
#import services  # [권장] : from apps.new_app import services
from .dto import ExampleDomainDTO  # [권장] : from apps.new_app.dto import ExampleDomainDTO


@swagger_auto_schema(
    method='post',
    request_body=ExampleDomainDTO,
    responses={201: ExampleDomainDTO},
    operation_description="Create a new example domain object"
)
@api_view(['GET', 'POST'])
def example_view(request):
    if request.method == 'GET':
        return services.example_view_get(request)
    elif request.method == 'POST':
        return services.example_view_post(request)
    else:
        raise Exception("Not supported method")


def example_template_view(request):
    return render(request, 'new_app/example.html', {'app_name': 'app_name'})
