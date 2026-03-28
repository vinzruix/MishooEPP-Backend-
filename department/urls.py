from django.urls import path

from department.views import DepartmentListApiView

urlpatterns = [
    path("api/department/", DepartmentListApiView.as_view())
]