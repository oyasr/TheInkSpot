from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter, SimpleRouter

from theinkspot.users.api.views import RegisterUsers, UserViewSet
from rest_framework_simplejwt import views as jwt_views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users/", UserViewSet, basename="users")


app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path("users/allusers/", UserViewSet.as_view({"get": "list"}), name="allusers"),
    path("users/register/", RegisterUsers.as_view(), name="register"),
    path('token/', jwt_views.TokenObtainPairView.as_view(),name='access token'),
    path('refresh/token/', jwt_views.TokenRefreshView.as_view(),name='refresh token'),
]
