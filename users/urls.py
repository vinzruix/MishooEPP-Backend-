from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users import views
from users.views import UserAPI

urlpatterns = [
    path("api/register/", UserAPI.as_view(), name="user_api"),
    path("api/token/", TokenObtainPairView.as_view(), name="get_token"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name='refresh'),

    path("api-auth/", include("rest_framework.urls")),
    path("temperatura/", views.temperatura)

]
