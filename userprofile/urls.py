from django.urls import path, include
from userprofile.views import index_page, UserDetailView, UserListView, add_user, delete_user


urlpatterns = [
    path('add/', add_user, name='add-user'),
    path('<slug:slug>/', UserListView.as_view(), name='user-list'),
    path('<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('delete/<int:id>', delete_user, name='delete-user'),
]
