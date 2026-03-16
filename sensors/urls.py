from django.urls import path

from sensors.views import SensorsCreateAPIView, TemperatureListAPIView, HumidityListAPIView, CO2ListAPIView, \
    TVOCListAPIView

urlpatterns = [
    path('api/sensors/', SensorsCreateAPIView.as_view()),
    path('api/sensors/temperature/', TemperatureListAPIView.as_view()),
    path('api/sensors/humidity/', HumidityListAPIView.as_view()),
    path('api/sensors/co2/', CO2ListAPIView.as_view()),
    path('api/sensors/tvoc/', TVOCListAPIView.as_view()),

]