from django.contrib import admin
from django.urls import path, include
from userprofile.views import index_page
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import handler404


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index_page, name="dashboard"),
    path('users/', include('userprofile.urls')),
    path('projects/', include('project.urls')),
    path('bugs/', include('bugs.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



handler404 = 'userprofile.views.page_not_found'
