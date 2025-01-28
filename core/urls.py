from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from core.swagger.schema import swagger_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('apps.users.urls_auth')),
    path('logistics/', include("apps.logistic.urls"))
]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

