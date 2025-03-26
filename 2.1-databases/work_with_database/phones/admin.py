from django.contrib import admin
from .models import Phone  # Импортируем модель

# Регистрируем модель
admin.site.register(Phone)
