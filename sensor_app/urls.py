from django.urls import path, include
from .views import SensorAPIView, LocationAPIView, LiveSensorAPIView, BlockchainValidityAPIView, CorrectBlockchainAPIView

urlpatterns = [
    path('sensorDataAPI/', SensorAPIView.as_view()),
    path('locationDataAPI/', LocationAPIView.as_view()),
    path('liveSensorData/', LiveSensorAPIView.as_view()),
    path('isChainValid/', BlockchainValidityAPIView.as_view()),
    path('correctBlockchain/', CorrectBlockchainAPIView.as_view()),
]