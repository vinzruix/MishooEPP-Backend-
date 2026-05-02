from django.urls import path

from attendance.views import AttendanceListAPIView, UserAttendanceDetailAPIView, NodeAttendanceDetailAPIView

urlpatterns = [
    path('api/attendance/', AttendanceListAPIView.as_view()),
    path('api/attendance/user/<int:pk>/', UserAttendanceDetailAPIView.as_view()),
    path('api/attendance/node/<str:pk>/', NodeAttendanceDetailAPIView.as_view()),

]