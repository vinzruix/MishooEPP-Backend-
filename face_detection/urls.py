from django.urls import path

from face_detection import views
from face_detection.views import CameraNodeCreateAPIView, EPPNodeDetailPatchDeleteAPIView

urlpatterns = [
    path('api/face_detection/', CameraNodeCreateAPIView.as_view()),
    path('api/face_detection/<str:camera_id>', EPPNodeDetailPatchDeleteAPIView.as_view()),

]