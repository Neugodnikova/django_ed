from django.shortcuts import render
from django.http import HttpResponse

DATA = {
    'omlet': {
        'яйца, шт': 2,
        'молоко, л': 0.1,
        'соль, ч.л.': 0.5,
    },
    'pasta': {
        'макароны, г': 0.3,
        'сыр, г': 0.05,
    },
    'buter': {
        'хлеб, ломтик': 1,
        'колбаса, ломтик': 1,
        'сыр, ломтик': 1,
        'помидор, ломтик': 1,
    },
}

def recipe_view(request, dish):
    if dish not in DATA:
        return HttpResponse("Такого рецепта нет.", status=404)

    servings = request.GET.get('servings', 1)

    try:
        servings = int(servings)
        if servings < 1:
            raise ValueError
    except ValueError:
        return HttpResponse("Некорректное значение servings. Укажите положительное целое число.", status=400)

    ingredients = {ingredient: amount * servings for ingredient, amount in DATA[dish].items()}

    context = {'recipe': ingredients}
    return render(request, 'calculator/index.html', context)
