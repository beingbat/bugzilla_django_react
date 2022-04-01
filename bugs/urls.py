from django.urls import path
from .views import *


urlpatterns = [
    path('view', view_bug, name='view-bug'),
]
