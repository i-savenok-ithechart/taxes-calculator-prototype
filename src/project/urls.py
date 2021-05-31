from django.contrib import admin
from django.urls import include, path

from common.api_exceptions_handling import handler404view, handler500view
from common.errors import do_error
from common.routers import DefaultRouter
from common.views import HealthView
from entities.invite.views import InviteViewSet
from entities.project.views import ProjectViewSet
from entities.scope.views import ScopeViewSet
from entities.scope_view.views import ScopeViewViewSet
from entities.space.views import SpaceViewSet
from entities.tag.views import TagViewSet
from entities.task.views import TaskViewSet
from entities.user.views import JWTObtainTOTPView, UserViewSet
from entities.user_event.views import UserEventViewSet
from project import settings

router = DefaultRouter()

router.register(r'users', UserViewSet, basename='users')
router.register(r'events', UserEventViewSet, basename='events')
router.register(r'invites', InviteViewSet, basename='invites')
router.register(r'spaces', SpaceViewSet, basename='spaces')
router.register(r'projects', ProjectViewSet, basename='projects')
router.register(r'scopes', ScopeViewSet, basename='scopes')
router.register(r'scope-views', ScopeViewViewSet, basename='scope-views')
router.register(r'tags', TagViewSet, basename='tags')
router.register(r'tasks', TaskViewSet, basename='tasks')

handler404 = handler404view
handler500 = handler500view

urlpatterns = [
    path(settings.API_URL_PREFIX, include(router.urls)),
    path(f'{settings.API_URL_PREFIX}token/', JWTObtainTOTPView.as_view()),

    path('admin/', admin.site.urls),
    path(f'{settings.API_URL_PREFIX}sentry-debug/', do_error),
    path('health/', HealthView.as_view()),
]
