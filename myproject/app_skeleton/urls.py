from django.urls import path
from . import views

urlpatterns = [
    path('example/', views.example_view, name='example'),
    path('example_template/', views.example_template_view, name='example_template'),
]