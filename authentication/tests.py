from django.test import TestCase
from .models import CustomUser

class CustomUserModelTest(TestCase):

    def setUp(self):
        # Set up a test user
        self.user = CustomUser.objects.create_user(
            aadhaar_number='123456789012',
            username='testuser',
            email='test@example.com',
            phone='1234567890',
            password='password123'
        )

    def test_user_creation(self):
        # Test if the user is created correctly
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertTrue(self.user.check_password('password123'))

    def test_user_str(self):
        # Test the string representation of the user
        self.assertEqual(str(self.user), 'testuser')
