from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from views.index_page import index_page

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("react", TemplateView.as_view(template_name="index.html")),
    path("", index_page, name="dashboard"),
    path("api/", include("api.urls")),
    path("users/", include("userprofile.urls")),
    path("projects/", include("project.urls")),
    path("bugs/", include("bugs.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = "views.error_page.page_not_found"
handler403 = "views.error_page.permission_denied"
handler400 = "views.error_page.bad_request"
handler500 = "views.error_page.server_error"
