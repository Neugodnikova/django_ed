from django.shortcuts import render
from django.core.paginator import Paginator
import csv
import os
from django.conf import settings

# Читаем CSV-файл с автобусными остановками
def get_bus_stations():
    file_path = os.path.join(settings.BASE_DIR, 'data-398-2018-08-30.csv')  # Путь к файлу
    with open(file_path, encoding='utf-8') as f:
        reader = csv.DictReader(f)
        return list(reader)

def index(request):
    # Данные для главной страницы, передаем их в шаблон
    bus_stations = get_bus_stations()  # Загружаем все станции
    paginator = Paginator(bus_stations, 10)  # Показываем по 10 записей на странице

    page_number = request.GET.get('page', 1)  # Получаем номер страницы из запроса
    page = paginator.get_page(page_number)  # Получаем объекты для текущей страницы

    return render(request, 'stations/index.html', {  # Передаем данные в шаблон
        'bus_stations': page,
        'page': page
    })

def bus_stations(request):
    bus_stations = get_bus_stations()
    paginator = Paginator(bus_stations, 10)  # Показываем по 10 записей на странице

    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    return render(request, 'stations/index.html', {  # Шаблон `index.html`, а не `stations.html`
        'bus_stations': page,
        'page': page
    })

