from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from face_detection.views import CameraNodeObtainPairSerializerAPIView, CameraNodeViewSet

urlpatterns = [
    path('api/face_detection/node/', CameraNodeViewSet.as_view({"get":"list","post":"create"})),
    path("api/face_detection/node/token/refresh/", TokenRefreshView.as_view()),
    path("api/face_detection/node/token/", CameraNodeObtainPairSerializerAPIView.as_view()),
    path('api/face_detection/node/<str:camera_id>/', CameraNodeViewSet.as_view({"patch":"partial_update","delete":"destroy"})),

]