from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient
from .models import Measurement, Sensor
from django.core.files.uploadedfile import SimpleUploadedFile


class MeasurementTests(TestCase):
    def setUp(self):
        """
        Этот метод выполняется перед каждым тестом.
        Он используется для настройки тестовых данных.
        """
        # Создаем тестовый сенсор
        self.sensor = Sensor.objects.create(name="Test Sensor")

        # Создаем пример изображения для теста
        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg')

        # Создаем APIClient для отправки запросов
        self.client = APIClient()

    def test_create_measurement(self):
        """Тестирование создания нового измерения"""
        url = '/api/v1/measurements/'
        data = {
            'sensor': self.sensor.id,
            'temperature': 23.5,
            'image': self.image
        }
        response = self.client.post(url, data, format='multipart')

        # Проверяем, что ответ возвращает статус 201 (создание)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что измерение сохранено в базе данных
        self.assertEqual(Measurement.objects.count(), 1)
        self.assertEqual(Measurement.objects.get().temperature, 23.5)

    def test_get_measurements(self):
        """Тестирование получения списка измерений"""
        # Создаем тестовое измерение
        measurement = Measurement.objects.create(
            sensor=self.sensor,
            temperature=22.5
        )

        url = '/api/v1/measurements/'
        response = self.client.get(url)

        # Проверяем, что ответ возвращает статус 200
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Проверяем, что полученные данные содержат созданное измерение
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['temperature'], 22.5)
