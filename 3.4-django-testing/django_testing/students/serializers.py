from rest_framework import serializers

from students.models import Course
from students.models import Student  # Импорт модели Student


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")



class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = ['id', 'name', 'course']  # Укажите необходимые поля модели Student

