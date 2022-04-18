from django.urls import path
from project.views import add_project, list_project, detail_project, delete_project

urlpatterns = [
  path('update/<int:pk>', add_project.UpdateProject.as_view(), name='update-project'),
  path('', list_project.ListProjects.as_view(), name='list-project'),
  path('<int:pk>', detail_project.DetailProject.as_view(), name='detail-project'),
  path('delete/<int:id>', delete_project.ProjectDelete.as_view(), name='delete-project'),
  path('add/', add_project.CreateProject.as_view(), name='add-project'),
]
