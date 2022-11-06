from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from datetime import date

from core.models import Order, Snack, Child, Classes
from order.serializers import OrderSerializer, ReadOrderSerializer

LIST_ORDER = reverse('list-order')
CREATE_ORDER = reverse('create-order')

def create_user(username: str = 'usertest', password: str = 'passwordtest') -> User:
    return User.objects.create_user(username=username, password=password)


def create_class(name: str = 'classtest') -> Classes:
    return Classes.objects.create(name=name)


def create_snack(name: str = 'snack1', price: float = 2.56) -> Snack:
    return Snack.objects.create(name=name, price=price)


def update_url(order_id: int) -> str:
    return reverse('update-order', args=[order_id])


def delete_url(order_id: int) -> str:
    return reverse('delete-order', args=[order_id])


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
        serializer = ReadOrderSerializer(orders, many=True)

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
    
    def test_create_order_error(self):
        """ test create order no exists child """
        snack1 = create_snack(name='juice')
        user2 = create_user(username='newuser', password='newpassword')

        child = Child.objects.create(code='NHELO2I4', name='testname', class_id=create_class(), father=user2)

        payload = {'order_day': 'qua', 'date': date(2022, 12, 23), 'child_id': child.id, 'snack_id': [snack1.id]}

        res = self.client.post(CREATE_ORDER, payload, format='json')
        
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_partial_update_order(self):
        """ test partial update an order """
        snack1 = create_snack()
        snack2 = create_snack(name='suco')

        child1 = Child.objects.create(code='NHELO2I4', name='testname', class_id=create_class(), father=self.user)

        order1 = Order.objects.create(order_day='seg', date=date(2022, 11, 16), child_id=child1)
        order1.snack_id.add(snack1.id)

        payload = {'date': date(2022, 11, 17), 'snack_id': [snack2.id]}

        url = update_url(order_id=order1.id)
        res = self.client.patch(url, payload, format='json')

        order1.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(order1.date, payload['date']) 
        self.assertEqual(order1.snack_id.get(id=snack2.id).id, snack2.id)
    
    def test_full_update_order(self):
        """ test full update an order, including exchange child """
        snack1 = create_snack()
        snack2 = create_snack(name='suco')

        child1 = Child.objects.create(code='NHELO2I4', name='testname', class_id=create_class(), father=self.user)
        child2 = Child.objects.create(code='NHELO2I7', name='testname1', class_id=create_class(), father=self.user)

        order = Order.objects.create(order_day='seg', date=date(2022, 11, 16), child_id=child1)
        order.snack_id.add(snack1.id)

        payload = {'date': date(2022, 12, 19), 'snack_id': [snack2.id], 'order_day': 'qua', 'child_id': child2.id}

        url = update_url(order_id=order.id)
        res = self.client.put(url, payload, format='json')

        order.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(order.date, payload['date'])
        self.assertEqual(order.child_id.id, child2.id)
        self.assertEqual(res.data['child_id'], child2.id)
        self.assertEqual(order.snack_id.count(), 1)
        self.assertEqual(order.snack_id.get(id=snack2.id).id, snack2.id)

    def test_update_order_erro(self):
        """ test update order other user error """
        snack1 = create_snack()
        snack2 = create_snack(name='suco')
        user2 = create_user(username='newuser', password='newpassword')

        child1 = Child.objects.create(code='NHELO2I4', name='testname', class_id=create_class(), father=user2)
        child2 = Child.objects.create(code='NHELO2I7', name='testname1', class_id=create_class(), father=self.user)

        order = Order.objects.create(order_day='seg', date=date(2022, 11, 16), child_id=child1)
        order.snack_id.add(snack1.id)

        payload = {'date': date(2022, 12, 19), 'snack_id': [snack2.id], 'order_day': 'qua', 'child_id': child2.id}

        url = update_url(order_id=order.id)
        res = self.client.put(url, payload, format='json')
        
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Order.objects.filter(id=order.id).exists())
    
    def test_delete_order_error(self):
        """ test delete order other user """
        snack1 = create_snack()
        user2 = create_user(username='newuser', password='newpassword')

        child1 = Child.objects.create(code='NHELO2I4', name='testname', class_id=create_class(), father=user2)

        order = Order.objects.create(order_day='seg', date=date(2022, 11, 16), child_id=child1)
        order.snack_id.add(snack1.id)

        url = delete_url(order_id=order.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertTrue(Order.objects.filter(id=order.id).exists())
    
    def test_delete_order(self):
        """ test delete order """
        snack1 = create_snack()

        child1 = Child.objects.create(code='NHELO2I4', name='testname', class_id=create_class(), father=self.user)

        order = Order.objects.create(order_day='seg', date=date(2022, 11, 16), child_id=child1)
        order.snack_id.add(snack1.id)

        url = delete_url(order_id=order.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        