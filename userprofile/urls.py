from django.urls import path, re_path
from .views import *


urlpatterns = [
    path('add/', CreateUserProfile.as_view(), name='add-user'),
    path('update/<int:id>', UpdateUserProfile.as_view(), name='update-user'),
    path('<slug:slug>/', UserListView.as_view(), name='user-list'),
    path('<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('delete/<int:id>', UserDelete.as_view(), name='delete-user'),
    re_path(
        r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,40})/$', activate, name='activate'),
]
