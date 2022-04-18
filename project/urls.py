from django.urls import path
from .views import *

urlpatterns = [
    path('add/', CreateProject.as_view(), name='add-project'),
    path('update/<int:pk>', UpdateProject.as_view(), name='update-project'),
    path('', ListProjects.as_view(), name='list-project'),
    path('<int:pk>', DetailProject.as_view(), name='detail-project'),
    path('delete/<int:id>', ProjectDelete.as_view(), name='delete-project'),
]
