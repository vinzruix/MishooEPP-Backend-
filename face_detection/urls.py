from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from face_detection import views
from face_detection.views import CameraNodeCreateAPIView, CameraNodeDetailPatchDeleteAPIView, \
    CameraNodeObtainPairSerializerAPIView

urlpatterns = [
    path('api/face_detection/node/', CameraNodeCreateAPIView.as_view()),
    path("api/face_detection/node/token/refresh/", TokenRefreshView.as_view()),
    path("api/face_detection/node/token/", CameraNodeObtainPairSerializerAPIView.as_view()),
    path('api/face_detection/node/<str:camera_id>/', CameraNodeDetailPatchDeleteAPIView.as_view()),

]