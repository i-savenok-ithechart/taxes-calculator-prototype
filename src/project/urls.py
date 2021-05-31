from django.contrib import admin
from django.urls import include, path

from common.errors import do_error
from common.routers import DefaultRouter
from common.views import HealthView
from project import settings

router = DefaultRouter()

urlpatterns = [
    path(settings.API_URL_PREFIX, include(router.urls)),

    path('admin/', admin.site.urls),
    path(f'{settings.API_URL_PREFIX}sentry-debug/', do_error),
    path('health/', HealthView.as_view()),
]
