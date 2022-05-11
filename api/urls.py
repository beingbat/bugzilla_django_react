from django.urls import path
from . import views

urlpatterns = [
    path("projects/", views.getProjectsList, name="list-projects-api"),
    path("users/<slug:slug>/", views.getUsersList, name="user-list-api"),
    path("bugs/", views.getBugsList, name="bug-list-api"),
    path("bugs/<slug>/", views.getBugsList, name="bug-list-api"),
    path("bugs/<slug>/<filter>/", views.getBugsList, name="bug-list-api"),
]
