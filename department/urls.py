from django.urls import path

from department.views import DepartmentViewSet, DepartmentSimpleViewSet

urlpatterns = [
    path("api/department/", DepartmentViewSet.as_view({"get":"list","post":"create"})),
    path("api/department/<int:department_id>/", DepartmentViewSet.as_view({"patch":"partial_update","delete":"destroy"})),
    path("api/department/simple/", DepartmentSimpleViewSet.as_view({"get":"list"}))

]