from django.shortcuts import render, get_object_or_404
from .models import Book

def books_view(request):
    """Отображение списка всех книг."""
    template = 'books/books_list.html'
    books = Book.objects.all().order_by('pub_date')  # Сортируем книги по дате
    context = {'books': books}
    return render(request, template, context)


def books_by_date_view(request, pub_date):
    """Отображение книг за конкретную дату с пагинацией на предыдущую и следующую дату."""
    template = 'books/books_by_date.html'
    
    books = Book.objects.filter(pub_date=pub_date)

    # Определяем предыдущую и следующую дату с книгами
    prev_date = Book.objects.filter(pub_date__lt=pub_date).order_by('-pub_date').first()
    next_date = Book.objects.filter(pub_date__gt=pub_date).order_by('pub_date').first()

    context = {
        'books': books,
        'prev_date': prev_date.pub_date if prev_date else None,
        'next_date': next_date.pub_date if next_date else None
    }
    return render(request, template, context)
