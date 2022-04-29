from django.urls import path

from theinkspot.users.views import user_detail_view, user_redirect_view, user_update_view
from theinkspot.users.api.views import RegisterUsers,UserViewSet

app_name = "users"
urlpatterns = [
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<int:id>/", view=user_detail_view, name="detail"),
    path('allusers/', UserViewSet.as_view({'get': 'list'}), name='allusers'),
    path('register/', RegisterUsers.as_view(), name='register')
]
