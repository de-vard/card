from django.test import TestCase
from django.urls import resolve
from . import views
from django.urls import reverse


class CardPageTest(TestCase):
    def test_uses_card_list_template(self):
        response = self.client.get(reverse('card:list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cards/index.html')

