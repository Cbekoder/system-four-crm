from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from core.swagger.generator import BothHttpAndHttpsSchemaGenerator

main_schema_view = get_schema_view(
    openapi.Info(
        title="System Service CRM API",
        default_version="v1",
        description="Business automation system",
        contact=openapi.Contact(email="cbekoder@gmail.com"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
    generator_class=BothHttpAndHttpsSchemaGenerator,
)
