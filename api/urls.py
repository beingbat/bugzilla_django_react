from django.urls import path
from . import views

urlpatterns = [
    path('/projects', views.getProjectsList, name='list-projects-api'),
]
