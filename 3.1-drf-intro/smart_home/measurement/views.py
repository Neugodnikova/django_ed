from rest_framework.generics import ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from .models import Sensor, Measurement
from .serializers import SensorSerializer, SensorDetailSerializer, MeasurementSerializer
from rest_framework import generics

# Создать и получить список датчиков
class SensorListCreateView(ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

# Получить информацию о конкретном датчике и обновить его
class SensorRetrieveUpdateView(RetrieveUpdateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorDetailSerializer

# Добавить измерение
class MeasurementCreateView(CreateAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer
class MeasurementListCreateView(generics.ListCreateAPIView):  # Разрешаем GET и POST
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer