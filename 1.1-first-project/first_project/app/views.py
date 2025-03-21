import os
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from datetime import datetime

def home_view(request):
    template_name = 'app/home.html'
    # Заполняем ссылки на другие страницы
    pages = {
        'Главная страница': reverse('home'),
        'Показать текущее время': reverse('time'),
        'Показать содержимое рабочей директории': reverse('workdir')
    }
    
    context = {
        'pages': pages
    }
    return render(request, template_name, context)


def time_view(request):
    # Получаем текущее время
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    msg = f'Текущее время: {current_time}'
    return HttpResponse(msg)


def workdir_view(request):
    # Получаем список файлов в рабочей директории
    workdir_files = os.listdir(os.getcwd())  # Текущая рабочая директория
    files_list = "\n".join(workdir_files)
    return HttpResponse(f"Содержимое рабочей директории:\n{files_list}")
