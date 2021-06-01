from django.urls import include, path

from common.admin import site as admin_site
from common.errors import do_error
from common.views import HealthView
from entities.tax.views import TaxView
from project import settings

api_urls = [
    path('taxes/', TaxView.as_view()),
]


urlpatterns = [
    path(settings.API_URL_PREFIX, include(api_urls)),

    path('admin/', admin_site.urls),
    path(f'{settings.API_URL_PREFIX}sentry-debug/', do_error),
    path('health/', HealthView.as_view()),
]
