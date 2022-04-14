from django.urls import path
from project.views import add_project, list_project, detail_project, delete_project

urlpatterns = [
  path('add/', add_project.add_project, name='add-project'),
  path('update/<int:id>', add_project.update_project, name='update-project'),
  path('', list_project.ListProjects.as_view(), name='list-project'),
  path('<int:pk>', detail_project.DetailProject.as_view(), name='detail-project'),
  path('delete/<int:id>', delete_project.delete_project, name='delete-project'),
]
