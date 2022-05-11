from django.urls import path
from . import views

urlpatterns = [
    path('/projects', views.getProjectsList, name='list-projects-api'),
    path('/users/<slug:slug>', views.getUsersList, name='user-list-api'),
]
