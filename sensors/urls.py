from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from sensors.views import TemperatureListAPIView, HumidityListAPIView, CO2ListAPIView, \
    TVOCListAPIView, \
    SensorNodeCreateAPIView, SensorNodeObtainPairSerializerAPIView, \
    SensorsDataCreateAPIView, SensorDataDetailAPIView

urlpatterns = [

    path("api/sensors/node/", SensorNodeCreateAPIView.as_view()),
    path("api/sensors/node/token/", SensorNodeObtainPairSerializerAPIView.as_view()),
    path("api/sensors/node/token/refresh/", TokenRefreshView.as_view()),

    path('api/sensors/', SensorsDataCreateAPIView.as_view()),

    path('api/sensors/temperature/', TemperatureListAPIView.as_view()),
    path('api/sensors/humidity/', HumidityListAPIView.as_view()),
    path('api/sensors/co2/', CO2ListAPIView.as_view()),
    path('api/sensors/tvoc/', TVOCListAPIView.as_view()),
    path('api/sensors/<str:sensor_node>/', SensorDataDetailAPIView.as_view()),

]