from django.test import TestCase
from django.urls import reverse

class RecipeTests(TestCase):
    def test_omlet_default_servings(self):
        response = self.client.get(reverse('recipe', args=['omlet']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'яйца, шт: 2')
        self.assertContains(response, 'молоко, л: 0.1')
        self.assertContains(response, 'соль, ч.л.: 0.5')

    def test_omlet_custom_servings(self):
        response = self.client.get(reverse('recipe', args=['omlet']) + '?servings=3')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'яйца, шт: 6')
        self.assertContains(response, 'молоко, л: 0.3')
        self.assertContains(response, 'соль, ч.л.: 1.5')

    def test_pasta_default_servings(self):
        response = self.client.get(reverse('recipe', args=['pasta']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'макароны, г: 0.3')
        self.assertContains(response, 'сыр, г: 0.05')

    def test_unknown_recipe(self):
        response = self.client.get(reverse('recipe', args=['pizza']))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Такого рецепта не знаю :(')
