from django.urls import path
from bugs.views import delete_bug, detail_bug, list_bug, assign_bug
from bugs.views.add_bug import *

urlpatterns = [
    path('update/<uuid:pk>', UpdateBug.as_view(), name='update-bug'),
    path('delete/<uuid:pk>', delete_bug.BugDelete.as_view(), name='delete-bug'),
    path('assignbug/<int:user_id>/<uuid:bug_id>', assign_bug.assign_bug, name='assign-bug'),
    path('<uuid:pk>', detail_bug.DetailBug.as_view(), name='detail-bug'),
    path('', list_bug.ListBug.as_view(), name='list-bug'),
    path('<slug>', list_bug.ListBug.as_view(), name='list-bug-filter'),
    path('<slug>/<filter>', list_bug.ListBug.as_view(), name='list-bug-filter'),
    path('add/<int:pk>/<slug:slug>', CreateBug.as_view(), name='add-bug'),
]
