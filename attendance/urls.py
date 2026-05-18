from django.urls import path

from attendance.views import AttendanceViewSet, UserAttendanceViewSet, NodeAttendanceViewSet

urlpatterns = [
    path('api/attendance/', AttendanceViewSet.as_view({"get":"list","post":"create"})),
    path('api/attendance/user/<int:pk>/', UserAttendanceViewSet.as_view({"get":"retrieve"})),
    path('api/attendance/node/<str:pk>/', NodeAttendanceViewSet.as_view({"get":"retrieve"})),

]