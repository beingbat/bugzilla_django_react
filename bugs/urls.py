from django.urls import path
from bugs.views import *

urlpatterns = [
    path('update/<uuid:pk>', UpdateBug.as_view(), name='update-bug'),
    path('delete/<uuid:pk>', BugDelete.as_view(), name='delete-bug'),
    path('assignbug/<int:user_id>/<uuid:bug_id>', assign_bug, name='assign-bug'),
    path('<uuid:pk>', DetailBug.as_view(), name='detail-bug'),
    path('', ListBug.as_view(), name='list-bug'),
    path('<slug>', ListBug.as_view(), name='list-bug-filter'),
    path('<slug>/<filter>', ListBug.as_view(), name='list-bug-filter'),
    path('add/<int:pk>/<slug:slug>', CreateBug.as_view(), name='add-bug'),
]
