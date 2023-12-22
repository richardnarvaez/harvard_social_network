from django.test import TestCase

# Create all tests unit this proyet here.

from network.models import User, Post, Profile, Like, Comment

def sumar(a, b):
    return a + b # 1.5 + 2.5 = 4.0
class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create(username='testuser', password='testpassword')

    def test_username_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Post.objects.create(user=User.objects.create(username='testuser', password='testpassword'), content='Test content')

    def test_content_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('content').verbose_name
        self.assertEqual(field_label, 'content')

class ProfileModelTest(TestCase):   
    def test_suma_decimal(self):
        self.assertEqual(sumar(1.5, 2.5), 4.0) 
