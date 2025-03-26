import csv
from django.core.management.base import BaseCommand
from phones.models import Phone
from django.utils.text import slugify


class Command(BaseCommand):
    help = 'Import phones from CSV file'

    def handle(self, *args, **options):
        file_path = 'phones.csv'  # Укажите правильный путь к файлу
        with open(file_path, encoding='utf-8') as file:
            reader = csv.DictReader(file, delimiter=';')
            for row in reader:
                phone, created = Phone.objects.get_or_create(
                    id=row['id'],
                    defaults={
                        'name': row['name'],
                        'price': float(row['price']),
                        'image': row['image'],
                        'release_date': row['release_date'],
                        'lte_exists': row['lte_exists'] == 'True',
                        'slug': slugify(row['name'])
                    }
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Добавлен телефон: {phone.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'Телефон уже существует: {phone.name}'))
