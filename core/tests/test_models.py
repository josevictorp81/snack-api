from django.contrib.auth.models import User
from django.test import TestCase
from datetime import date

from core.models import Classes, Snack, Child, Order


def create_user(username: str, password: str):
    return User.objects.create_user(username=username, password=password)

class ModelTests(TestCase):
    def test_create_user(self):
        """ test create user successfull """
        username = 'usernametest'
        password = 'testpassword00'
        user = create_user(username=username, password=password)
        
        self.assertEqual(user.username, username)
        self.assertTrue(user.check_password(password))
        self.assertEqual(user.__str__(), user.username)
    
    def test_classes_str(self):
        """ test str Classes """
        c = Classes.objects.create(name='1° serie')

        self.assertEqual(c.__str__(), c.name)
    
    def test_snack_str(self):
        """ test str snack """
        snack = Snack.objects.create(name='refri', price=2.5)

        self.assertEqual(snack.__str__(), 'refri')
    
    def test_child_str(self):
        """ test str child """
        user = create_user(username='usernametest', password='testpassword00')
        classe = Classes.objects.create(name='classtest')
        child = Child.objects.create(name='nometest', code='OIRB', class_id=classe, father=user)

        self.assertEqual(child.__str__(), 'nometest')
    
    def test_order_str(self):
        """ test str order """
        user = create_user(username='usernametest', password='testpassword00')
        classe = Classes.objects.create(name='classtest')
        Child.objects.create(name='nometest', code='OIRB', class_id=classe, father=user)
        snack = Snack.objects.create(name='refri', price=2.5)
        snack1 = Snack.objects.create(name='suco', price=2.7)

        child = Child.objects.get(father=user.id)

        order = Order.objects.create(date=date(2022, 11, 5), child_id=child, order_value=12.25)
        order.snack_id.add(snack.id, snack1.id)

        self.assertEqual(order.__str__(), f'Order id: {order.id}')

