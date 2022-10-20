from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model

from core.models import Snack

LIST_SNACK = reverse('list-snack')

class PrivateSnackApiTest(APITestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(username='usertest', password='passwordtest')
        self.client.force_authenticate(user=self.user)
    
    def test_list_all_snack(self):
        """ test list all snacks """
        Snack.objects.create(name='snack 1', price=3.29)
        Snack.objects.create(name='snack 2', price=6.78)

        res = self.client.get(LIST_SNACK)
        c = Snack.objects.all().count()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(c, 2)
    
    def test_post_not_allowed(self):
        """ test post method not allowed """
        payload = {'name': 'snack 1', 'price': 3.29}

        res = self.client.post(LIST_SNACK, payload, formt='json')

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        