from django.urls import path, re_path
from .views import *

urlpatterns = [
  path('add/<int:id>', add_bug, name='add-bug'),
  path('update/<uuid>', update_bug, name='update-bug'),
  path('delete/<uuid>', delete_bug, name='delete-bug'),
  path('<uuid:pk>', DetailBug.as_view(), name='detail-bug'),
  path('', ListBug.as_view(), name='list-bug'),
]
