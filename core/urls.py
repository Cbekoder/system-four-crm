from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from apps.main.views import RedirectToDocs
from core.swagger.schema import swagger_urlpatterns

urlpatterns = [
    path('', RedirectToDocs),
    path('admin/', admin.site.urls),
<<<<<<< HEAD
    path('auth/', include('apps.users.urls_auth')),
    path('logistics/', include("apps.logistic.urls")),
    path('general/', include("apps.main.urls")),
    path('mixed/', include("apps.main.urls_mix")),
=======
    path('api/v1/common/', include("apps.users.urls")),
    path('garden/', include("apps.garden.urls")),
>>>>>>> 291ccae (updated)
]

urlpatterns += swagger_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

