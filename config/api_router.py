from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from theinkspot.users.api.views import UserViewSet,RegisterUsers
from django.urls import path
if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users/", UserViewSet, basename='users')


app_name = "api"
urlpatterns = router.urls

urlpatterns += [
    path('users/allusers/', UserViewSet.as_view({'get': 'list'}), name='allusers'),
    path('users/register/', RegisterUsers.as_view(), name='register')
]