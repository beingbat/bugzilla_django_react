from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from userprofile.views import index_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', index_page, name="dashboard"),
    path('users/', include('userprofile.urls')),
    path('projects/', include('project.urls')),
    path('bugs/', include('bugs.urls')),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)



handler404 = 'userprofile.views.page_not_found'
handler403 = 'userprofile.views.permission_denied'
handler400 = 'userprofile.views.bad_request'
handler500 = 'userprofile.views.server_error'
