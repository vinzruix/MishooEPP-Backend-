from django.urls import path

from incidence.views import IncidenceViewSet

urlpatterns = [
    path("api/incidence/", IncidenceViewSet.as_view({"get":"list","post":"create"})),
    path("api/incidence/<str:epp_node_id>", IncidenceViewSet.as_view({"get":"retrieve"}))
]