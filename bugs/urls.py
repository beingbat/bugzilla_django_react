from django.urls import path
from .views import *

urlpatterns = [
    path('add/<int:id>', add_bug, name='add-bug'),
    path('update/<uuid:pk>', update_bug, name='update-bug'),
    path('delete/<uuid:pk>', delete_bug, name='delete-bug'),
    path('assignbug/<int:user_id>/<uuid:bug_id>', assign_bug, name='assign-bug'),
    path('<uuid:pk>', DetailBug.as_view(), name='detail-bug'),
    path('', ListBug.as_view(), name='list-bug'),
]
