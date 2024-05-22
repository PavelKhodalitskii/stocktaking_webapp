from django.test import TestCase
from django.urls import reverse

from account.models import OfficeBuilding, CustomUser

class TestReportsViewsAvailible(TestCase):
    office_building = None
    superuser = None

    def get_test_user(self):
        if self.superuser:
            return self.superuser
        self.superuser = CustomUser(username='admin', is_staff=True, is_active=True)
        self.superuser.set_password("admin")
        self.client.login(username='admin', password='admin')
        self.superuser.save()
        return self.superuser

    def get_test_office_building(self):
        if self.office_building:
            return self.office_building
        else:
            self.office_building = OfficeBuilding(slug='en_plus_digital', address="ул. Нижняя Набережная, 14, Иркутск, Иркутская обл., 664011")
            self.office_building.save()
        return self.office_building

    def test_reports_view_avalible(self):
        test_office = self.get_test_office_building()
        self.get_test_user()
        self.client.login(username='admin', password='admin')
        response = self.client.get(reverse('reports', kwargs={'officebuilding_slug': test_office.slug}))
        self.assertEqual(response.status_code, 200)