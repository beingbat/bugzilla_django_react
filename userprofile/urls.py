from django.urls import path, re_path
from userprofile.views.activate_user import *
from userprofile.views.add_user import *
from userprofile.views.delete_user import *
from userprofile.views.detail_user import *
from userprofile.views.list_user import *

urlpatterns = [
    path('add/', add_user, name='add-user'),
    path('update/<int:id>', update_user, name='update-user'),
    path('<slug:slug>/', UserListView.as_view(), name='user-list'),
    path('<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('delete/<int:id>', UserDelete.as_view(), name='delete-user'),
    re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$', activate, name='activate'),
]
