from django.test import TestCase
from django.urls import reverse
from django.contrib import auth

from account.models import OfficeBuilding, CustomUser
from items_management.models import InventoryItems

class TestItemsViewsAvailible(TestCase):
    office_building = None
    item = None
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
    

    def get_test_item(self):
        if self.item:
            return self.item
        else:
            self.item = InventoryItems(
                                item_number=1, 
                                slug=f"placeholder_{1}", 
                                name="Placeholder",
                                )
            self.item.save()
        return self.item
            
    def test_items_list_view_avalible(self):
        test_office = self.get_test_office_building()
        self.get_test_user()
        self.client.login(username='admin', password='admin')
        url = reverse('items_list', kwargs={'officebuilding_slug': test_office.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_items_detail_view_avalible(self):
        test_office = self.get_test_office_building()
        item = self.get_test_item()
        self.get_test_user()
        self.client.login(username='admin', password='admin')

        url = reverse('item_detail', kwargs={'officebuilding_slug': test_office.slug, 'item_slug': item.slug})

        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)