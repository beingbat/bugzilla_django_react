from django.urls import path

from .views import ListBugs, ListProjects, ListProfiles

urlpatterns = [
    path("projects/", ListProjects.as_view(), name="list-projects-api"),
    path("users/<slug:slug>/", ListProfiles.as_view(), name="user-list-api"),
    path("bugs/", ListBugs.as_view(), name="bug-list-api"),
    path("bugs/<slug>/", ListBugs.as_view(), name="bug-list-api"),
    path("bugs/<slug>/<filter>/", ListBugs.as_view(), name="bug-list-api"),
]
