from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

from core.models import Order, Snack, Child, Classes
from order.serializers import OrderSerializer

LIST_ORDER = reverse('list-order')
CREATE_ORDER = reverse('create-order')

def create_user(username: str = 'usertest', password: str = 'passwordtest'):
    return User.objects.create_user(username=username, password=password)


def create_class(name: str = 'classtest'):
    return Classes.objects.create(name=name)


def create_snack(name: str = 'snack1', price: float = 2.56):
    return Snack.objects.create(name=name, price=price)


class PublicOderApiTest(APITestCase):

    def test_list_order(self):
        """ test list order unauthorized """
        res = self.client.get(LIST_ORDER)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateOderApiTest(APITestCase):
    def setUp(self) -> None:
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_list_order(self):
        """ test list order filter by child of authentication user """
        user2 = create_user(username='seconduser', password='testserpass')
        snack1 = create_snack()
        snack2 = create_snack(name='snack2')

        child1 = Child.objects.create(code='NHELO2I4', name='testname', class_id=create_class(), father=self.user)
        child2 = Child.objects.create(code='NHELO2I7', name='testname1', class_id=create_class(), father=user2)

        order1 = Order.objects.create(order_day='seg', date=date(2022, 11, 16), child_id=child1)
        order1.snack_id.add(snack1.id, snack2.id)
        order2 = Order.objects.create(order_day='seg', date=date(2022, 11, 16), child_id=child2)
        order2.snack_id.add(snack1.id, snack2.id)

        res = self.client.get(LIST_ORDER)
        orders = Order.objects.filter(child_id__father=self.user)
        serializer = OrderSerializer(orders, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data, serializer.data)
    
    def test_create_order_success(self):
        """ test create a order successful """
        snack1 = create_snack(name='juice')
        snack2 = create_snack(name='apple')

        child = Child.objects.create(code='NHO3UD5G', name='whatever', class_id=create_class(), father=self.user)

        payload = {'order_day': 'qua', 'date': date(2022, 12, 23), 'child_id': child.id, 'snack_id': [snack1.id, snack2.id]}

        res = self.client.post(CREATE_ORDER, payload, format='json')

        order = Order.objects.filter(id=res.data['id'])
        
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(order.exists())
        self.assertTrue(res.data['order_value'])