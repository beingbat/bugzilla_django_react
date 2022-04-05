from django.urls import path
from userprofile.views import UserDetailView, UserListView, add_user, delete_user, update_user


urlpatterns = [
    path('add/', add_user, name='add-user'),
    path('update/<int:id>', update_user, name='update-user'),
    path('<slug:slug>/', UserListView.as_view(), name='user-list'),
    path('<int:pk>', UserDetailView.as_view(), name='user-detail'),
    path('delete/<int:id>', delete_user, name='delete-user'),
]
