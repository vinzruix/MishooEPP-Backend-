from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from epp_detection.views import EPPNodeListCreateAPIView, EPPNodeObtainPairSerializerAPIView, \
    EPPNodeDetailPatchDeleteAPIView

urlpatterns = [

    path("api/epp_detection/node/", EPPNodeListCreateAPIView.as_view()),
    path("api/epp_detection/node/token/", EPPNodeObtainPairSerializerAPIView.as_view()),
    path("api/epp_detection/node/token/refresh/", TokenRefreshView.as_view()),
    path("api/epp_detection/node/<str:epp_node_id>/", EPPNodeDetailPatchDeleteAPIView.as_view()),

]