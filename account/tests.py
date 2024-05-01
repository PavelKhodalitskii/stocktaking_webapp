from django.test import TestCase

from .models import CustomUser, Office, OfficeBuilding
# Create your tests here.

# class OfficeBuildingTest(TestCase):
#     def test_create_office_building(self):


class TestCustomUserModels(TestCase):
    # def test_create_user(self):
    #     user = CustomUser(username='username_1', first_name="Name", second_name="LastName", is_active=True)
    #     user.set_password("password")
    #     user.save()
    #     user = CustomUser(username='username_2', first_name="Name", second_name="LastName", is_active=False)
    #     user.set_password("password")
    #     user.save()
    #     print("PASSED")

    def test_create_superuser(self):
        try:
            superuser = CustomUser(username='admin', is_staff=True, is_active=True)
            superuser.set_password("admin")
            superuser.save()
        except Exception as e:
            self.fail(e)
        print("PASSED")

    