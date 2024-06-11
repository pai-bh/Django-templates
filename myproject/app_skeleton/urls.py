from django.urls import path
from . import views


app_name = 'CHANGEME'
urlpatterns = [
    path('example/', views.example_view, name='example'),
    path('example_template/<int:model_id>', views.example_template_view, name='example_template'),
]