from django.urls import path

from .views import (
    BugCollectionAPIView,
    ProjectCollectionAPIView,
    ProfileCollectionAPIView,
)

urlpatterns = [
    path("projects/", ProjectCollectionAPIView.as_view(), name="list-projects-api"),
    path(
        "users/<slug:slug>/", ProfileCollectionAPIView.as_view(), name="user-list-api"
    ),
    path("bugs/", BugCollectionAPIView.as_view(), name="bug-list-api"),
    path("bugs/<slug>/", BugCollectionAPIView.as_view(), name="bug-list-api"),
    path("bugs/<slug>/<filter>/", BugCollectionAPIView.as_view(), name="bug-list-api"),
]
