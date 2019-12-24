from django.conf import settings
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views import defaults as default_views
from rest_framework.permissions import AllowAny
from rest_framework.routers import DefaultRouter
from fcm_django.api.rest_framework import FCMDeviceAuthorizedViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from .drf_yasg_custom import CustomOpenAPISchemaGenerator


schema_view = get_schema_view(
    openapi.Info(
        title="Rest APIs Phasma Food",
        default_version='v2',
        description="""The main objective of the PhasmaFOOD is to design and implement a multi-target food 
        sensitive mini-portable system for on-the-spot food quality sensing and shelf-life prediction. 
        The PhasmaFOOD miniaturized smart integrated system will be able to detect food hazards, 
        spoilage -including early signs of spoilage-, and food fraud through heterogeneous micro-scale photonics. 
        The connected device will be integrated with a parameterized, knowledge-based, 
        software architecture for on-the-spot food quality sensing and shelf-life prediction.""",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="predrag.orelj@vizlore.com"),
        license=openapi.License(name="Apache Software License 2.0"),
    ),
    public=False,
    permission_classes=(AllowAny,),
    generator_class=CustomOpenAPISchemaGenerator,
)

router = DefaultRouter()
router.register(r'firebase', FCMDeviceAuthorizedViewSet)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path(settings.ADMIN_URL, admin.site.urls),
    path("api/v2/accounts/", include("rest_auth.urls")),
    path("api/v2/accounts/registration/", include("rest_auth.registration.urls")),
    path("api/v2/samples/", include("phasma_food_v2.samples.urls")),
    path("api/v2/statistic/", include("phasma_food_v2.statistic.urls")),
    path("api/v2/mobile/", include("phasma_food_v2.measurements.urls")),
    path("api/v2/phasma/", include("phasma_food_v2.devices.urls")),
    path("api/v2/dashboard/", include("phasma_food_v2.dashboard.urls")),
    path("api/v2/", include(router.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
