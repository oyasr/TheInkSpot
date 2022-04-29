from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from theinkspot.users.api.views import UserViewSet,RegisterUsers

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

# router.register("allusers/", UserViewSet, basename='users')
# router.register("register/", RegisterUsers, basename='register')


app_name = "api"
urlpatterns = router.urls
