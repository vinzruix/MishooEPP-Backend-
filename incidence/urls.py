from django.urls import path

from incidence.views import IncidenceCreateListApiView, IncidenceDetailPatchDelete

urlpatterns = [
    path("api/incidence/", IncidenceCreateListApiView.as_view()),
    path("api/incidence/<str:epp_node_id>", IncidenceDetailPatchDelete.as_view())
]