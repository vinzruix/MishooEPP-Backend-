from django.conf.urls.static import static
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from MishooEPP_Backend import settings
from users import views
from users.views import *

urlpatterns = [
    path("api/users/", UserListCreateAPIView.as_view(), name="UserListCreateAPIView"),
    path("api/users/<int:pk>", UserDetailAPIView.as_view(), name="UserDetailAPIView"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='refresh'),

    path("api-auth/", include("rest_framework.urls")),


]


