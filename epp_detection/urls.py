from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from epp_detection.views import EPPNodeViewSet, EPPNodeObtainPairSerializerAPIView

urlpatterns = [

    path("api/epp_detection/node/", EPPNodeViewSet.as_view({"get":"list","post":"create"})),
    path("api/epp_detection/node/token/", EPPNodeObtainPairSerializerAPIView.as_view()),
    path("api/epp_detection/node/token/refresh/", TokenRefreshView.as_view()),
    path("api/epp_detection/node/<str:epp_node_id>/", EPPNodeViewSet.as_view({"get":"retrieve","patch":"partial_update","delete":"destroy"})),

]