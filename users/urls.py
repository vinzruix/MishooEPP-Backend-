from django.urls import path, include
from rest_framework_simplejwt.views import  TokenRefreshView

from users.views import *

urlpatterns = [
    path("api/users/", UserViewSet.as_view({"get":"list","post":"create"})),
    path("api/users/<int:pk>/", UserViewSet.as_view({"get":"retrieve"})),
    path("api/token/", CustomTokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='refresh'),
    path("api-auth/", include("rest_framework.urls")),


]


