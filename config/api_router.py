from posixpath import basename
from django.urls import path

from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from theinkspot.users.api.views import UserViewSet
from rest_framework_simplejwt import views as jwt_views


if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet,basename='UserViewSet')



app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path('token/', jwt_views.TokenObtainPairView.as_view(),name='access token'),
    path('refresh/token/', jwt_views.TokenRefreshView.as_view(),name='refresh token'),
]
