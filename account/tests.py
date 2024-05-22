from django.test import TestCase
from django.urls import reverse

from .models import CustomUser, Office, OfficeBuilding

class TestCustomUserModels(TestCase):
    def test_create_superuser(self):
        try:
            superuser = CustomUser(username='admin', is_staff=True, is_active=True)
            superuser.set_password("admin")
            self.client.login(username='admin', password='admin')
            superuser.save()
        except Exception as e:
            self.fail(e)


class AccountViewsTest(TestCase):
    def test_user_login_availible(self):
        response = self.client.get(reverse('site_login'))
        self.assertEqual(response.status_code, 200)

    def test_register_user_availible(self):
        response = self.client.get(reverse('site_register'))
        self.assertEqual(response.status_code, 200)


    