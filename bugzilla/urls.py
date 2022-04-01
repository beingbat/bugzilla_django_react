from django.contrib import admin
from django.urls import path, include
from userprofile.views import index_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index_page, name="dashboard"),
    path('users/', include('userprofile.urls')),
    path('projects/', include('project.urls')),
]
