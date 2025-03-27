import pytest
from rest_framework import status
from model_bakery import baker
from django.urls import reverse
from rest_framework.test import APIClient
from students.models import Course, Student

@pytest.fixture
def api_client():
    """Фикстура для клиента API"""
    return APIClient()

@pytest.fixture
def course_factory():
    """Фикстура для создания курса"""
    return baker.make(Course)  # Создаем курс через baker.make

@pytest.fixture
def student_factory():
    """Фикстура для создания студента"""
    return baker.make(Student)  # Создаем студента через baker.make

@pytest.mark.django_db
def test_get_course(api_client, course_factory):
    """Тест для получения одного курса"""
    course = baker.make(Course)  # Используем baker для создания курса
    url = reverse('courses-detail', kwargs={'pk': course.id})  # Строим URL для запроса
    response = api_client.get(url)  # Делаем GET-запрос

    assert response.status_code == status.HTTP_200_OK  # Проверяем успешный ответ
    assert response.data['id'] == course.id  # Проверяем, что вернулся именно тот курс
    assert response.data['name'] == course.name  # Проверяем, что имя курса совпадает

@pytest.mark.django_db
def test_get_courses_list(api_client, course_factory):
    """Тест для получения списка курсов"""
    course1 = baker.make(Course)  # Создаем первый курс
    course2 = baker.make(Course)  # Создаем второй курс
    url = reverse('courses-list')  # Строим URL для списка курсов
    response = api_client.get(url)  # Делаем GET-запрос

    assert response.status_code == status.HTTP_200_OK  # Проверяем успешный ответ
    assert len(response.data) >= 2  # Проверяем, что возвращается хотя бы два курса
    assert any(course['id'] == course1.id for course in response.data)  # Проверяем наличие первого курса
    assert any(course['id'] == course2.id for course in response.data)  # Проверяем наличие второго курса

@pytest.mark.django_db
@pytest.mark.parametrize('filter_param, expected_count', [
    ('id', 1), 
    ('name', 1),
])
def test_filter_courses(api_client, course_factory, filter_param, expected_count):
    """Тест для фильтрации курсов по ID или имени"""
    course1 = baker.make(Course, name="Course 1")  # Создаем курс с именем "Course 1"
    course2 = baker.make(Course, name="Course 2")  # Создаем курс с именем "Course 2"
    
    # Применяем фильтрацию
    if filter_param == 'id':
        url = reverse('courses-list') + f'?id={course1.id}'
    else:
        url = reverse('courses-list') + f'?name=Course 1'
        
    response = api_client.get(url)  # Делаем GET-запрос с фильтром

    assert response.status_code == status.HTTP_200_OK  # Проверяем успешный ответ
    assert len(response.data) == expected_count  # Проверяем, что вернулось количество курсов
    if filter_param == 'id':
        assert response.data[0]['id'] == course1.id  # Проверяем, что это тот курс, который мы запрашивали
    else:
        assert response.data[0]['name'] == "Course 1"  # Проверяем, что это курс с правильным именем

@pytest.mark.django_db
def test_create_course(api_client):
    """Тест для успешного создания курса"""
    data = {"name": "New Course"}  # Данные для создания курса
    url = reverse('courses-list')  # Строим URL для создания нового курса
    response = api_client.post(url, data, format='json')  # Делаем POST-запрос

    assert response.status_code == status.HTTP_201_CREATED  # Проверяем, что курс был создан
    assert response.data['name'] == "New Course"  # Проверяем, что имя курса правильно
    assert 'id' in response.data  # Проверяем, что возвращается id нового курса

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    """Тест для успешного обновления курса"""
    course = baker.make(Course, name="Old Name")  # Создаем курс с старым именем
    data = {"name": "Updated Course"}  # Данные для обновления
    url = reverse('courses-detail', kwargs={'pk': course.id})  # Строим URL для обновления курса
    response = api_client.put(url, data, format='json')  # Делаем PUT-запрос

    assert response.status_code == status.HTTP_200_OK  # Проверяем, что курс был обновлен
    assert response.data['name'] == "Updated Course"  # Проверяем, что имя курса обновилось

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    """Тест для успешного удаления курса"""
    course = baker.make(Course)  # Создаем курс
    url = reverse('courses-detail', kwargs={'pk': course.id})  # Строим URL для удаления курса
    response = api_client.delete(url)  # Делаем DELETE-запрос

    assert response.status_code == status.HTTP_204_NO_CONTENT  # Проверяем успешный ответ
    assert not Course.objects.filter(id=course.id).exists()  # Проверяем, что курс удален из базы

@pytest.mark.django_db
@pytest.mark.parametrize('max_students', [20])  # Параметризуем максимальное количество студентов
def test_max_students_on_course(api_client, course_factory, student_factory, max_students):
    """Тест для проверки ограничения на максимальное число студентов"""
    course = baker.make(Course)  # Создаем курс через baker
    # Создаем студентов для курса
    for _ in range(max_students):
        baker.make(Student, course=course)  # Создаем студентов для курса
        
    # Попробуем создать студента, если курс уже заполнен
    response = api_client.post(reverse('students-list'), {'course': course.id, 'name': 'New Student'}, format='json')
    
    if course.students.count() >= max_students:
        assert response.status_code == status.HTTP_400_BAD_REQUEST  # Проверяем, что больше нельзя добавить
    else:
        assert response.status_code == status.HTTP_201_CREATED  # Проверяем, что студент добавлен
