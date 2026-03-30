from django.urls import path

from face_detection import views
from face_detection.views import FaceDetectionCreateAPIView

urlpatterns = [
    path('api/face_detection/', FaceDetectionCreateAPIView.as_view())

]