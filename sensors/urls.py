from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from sensors.views import TemperatureListAPIView, HumidityListAPIView, CO2ListAPIView, \
    TVOCListAPIView, \
    SensorNodeListCreateAPIView, SensorNodeObtainPairSerializerAPIView, \
    SensorsDataCreateAPIView, SensorDataDetailAPIView, SensorNodeDetailPatchAPIView

urlpatterns = [

    path("api/sensors/node/", SensorNodeListCreateAPIView.as_view()),
    path("api/sensors/node/token/", SensorNodeObtainPairSerializerAPIView.as_view()),
    path("api/sensors/node/token/refresh/", TokenRefreshView.as_view()),
    path("api/sensors/node/<str:sensor_node_id>/", SensorNodeDetailPatchAPIView.as_view()),

    path('api/sensors/', SensorsDataCreateAPIView.as_view()),

    path('api/sensors/temperature/', TemperatureListAPIView.as_view()),
    path('api/sensors/humidity/', HumidityListAPIView.as_view()),
    path('api/sensors/co2/', CO2ListAPIView.as_view()),
    path('api/sensors/tvoc/', TVOCListAPIView.as_view()),
    path('api/sensors/<str:sensor_node_id>/', SensorDataDetailAPIView.as_view()),

]