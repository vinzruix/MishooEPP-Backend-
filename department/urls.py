from django.urls import path

from department.views import DepartmentListApiView, DepartmentListSimpleApiView, DepartmentDetailApiView

urlpatterns = [
    path("api/department/", DepartmentListApiView.as_view()),
    path("api/department/<int:department_id>/", DepartmentDetailApiView.as_view()),
    path("api/department/simple/", DepartmentListSimpleApiView.as_view())

]