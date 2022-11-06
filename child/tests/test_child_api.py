from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User

from core.models import Child, Classes
from child.serializers import ChildSerializer, ReadChildSerializer
from child.utils import generate_code

LIST_CHILD_URL = reverse('list-child')
CREATE_CHILD_URL = reverse('create-child')

def create_user(**params):
    return User.objects.create_user(**params)


def create_class(name: str = 'classtest'):
    return Classes.objects.create(name=name)


class PublicChildApiTest(APITestCase):
    def test_retrieve_unauthorized(self):
        """ test authentication requid """
        res = self.client.get(LIST_CHILD_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateChildApiTest(APITestCase):
    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user(username='usertest', password='passwordtest')
        self.client.force_authenticate(user=self.user)
    
    def test_list_child(self):
        """ test list child filter by authenticated user """
        c = create_class()
        user2 = create_user(username='usertest2', password='passwordtest')

        Child.objects.create(name='nametest1', code=generate_code(), class_id=c, father=self.user)
        Child.objects.create(name='nametest2', code=generate_code(), class_id=c, father=user2)

        res = self.client.get(LIST_CHILD_URL)
        childs = Child.objects.filter(father=self.user)
        serializer = ReadChildSerializer(childs, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
    
    def test_create_child_success(self):
        """ test create child success """
        c = create_class()
        payload = {'name': 'nametest', 'class_id': c.id}

        res = self.client.post(CREATE_CHILD_URL, payload, format='json')
        child = Child.objects.get(id=res.data['id'])
        serializer = ChildSerializer(child)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data, serializer.data)
        
    def test_create_child_error(self):
        """ test create child with no exist class """
        payload = {'name': 'nametest', 'class_id': 5}

        res = self.client.post(CREATE_CHILD_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_child_no_parameter(self):
        """ test create child no parameter """
        res = self.client.post(CREATE_CHILD_URL, {}, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_child_wrong_parameter(self):
        """ test create child with wrong parameter """
        payload = {'name': 2, 'class_id': 'class'}

        res = self.client.post(CREATE_CHILD_URL, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    