from django.urls import path

from department.views import DepartmentListApiView, DepartmentListSimpleApiView

urlpatterns = [
    path("api/department/", DepartmentListApiView.as_view()),
    path("api/department/simple/", DepartmentListSimpleApiView.as_view())

]