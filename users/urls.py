from django.urls import path, include
from rest_framework_simplejwt.views import  TokenRefreshView

from users.views import *

urlpatterns = [
    path("api/users/", UserListCreateAPIView.as_view(), name="UserListCreateAPIView"),
    path("api/users/all/", AllUsersAPIView.as_view(), name="AllUsersDetailAPIView"),
    path("api/users/<int:pk>/", UserDetailAPIView.as_view(), name="UserDetailAPIView"),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='refresh'),

    path("api-auth/", include("rest_framework.urls")),


]


