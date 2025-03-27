from django.views.generic import ListView
from .models import Student

class StudentListView(ListView):
    model = Student
    template_name = 'school/students_list.html'
    context_object_name = 'object_list'

    def get_queryset(self):
        # Используем prefetch_related для оптимизации запросов
        return Student.objects.prefetch_related('teachers').order_by('group')

