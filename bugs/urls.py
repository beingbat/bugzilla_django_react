from django.urls import path
from .views import *

urlpatterns = [
  path('add/<int:id>', add_bug, name='add-bug'),
  path('update/<int:id>', update_bug, name='update-bug'),
  path('', ListBug.as_view(), name='list-bug'),
  path('<int:pk>', DetailBug.as_view(), name='detail-bug'),
  path('delete/<int:id>', delete_bug, name='delete-bug'),
]
