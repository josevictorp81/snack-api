from django.contrib.auth.models import User
from django.test import TestCase

from core.models import Classes, Snack


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