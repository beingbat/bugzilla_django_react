from django.urls import path
from project.views import *

urlpatterns = [
  path('add/', add_project, name='add-project'),
  path('update/<int:id>', update_project, name='update-project'),
  path('', ListProjects.as_view(), name='list-project'),
  path('<int:pk>', DetailProject.as_view(), name='detail-project'),
  path('delete/<int:id>', delete_project, name='delete-project'),
]
