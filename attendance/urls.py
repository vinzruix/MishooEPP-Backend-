from django.urls import path

from attendance.views import AttendanceListAPIView

urlpatterns = [
    path('api/attendance/', AttendanceListAPIView.as_view())
]