from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from core.models import Classes

LIST_CLASSES = reverse('list-class')

class PrivateClassesApiTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(username='usertest', password='passwordtest')
        self.client.force_authenticate(user=self.user)
    
    def test_list_all_classes(self):
        """ test list all classes """
        Classes.objects.create(name='class1')
        Classes.objects.create(name='class2')

        res = self.client.get(LIST_CLASSES)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
    
    def test_post_not_allowed(self):
        """ test post method not allowed """
        payload = {'name': 'class1'}

        res = self.client.post(LIST_CLASSES, payload, formt='json')

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
