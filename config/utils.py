from account.models import CustomUser, OfficeBuilding, Office
from items_management.models import InventoryItems

def debug_prepare():
    print("Preparing for debug")

    superuser = ''
    try: 
        superuser = CustomUser.objects.get(username="admin")
    except:
        superuser = CustomUser(username="admin", is_staff=True, is_active=True)
        superuser.set_password("admin")
        superuser.save()

    office_building = ''
    try:
        office_building = OfficeBuilding.objects.get(pk=1)
    except:
        office_building = OfficeBuilding(slug='en_plus_digital', address="ул. Нижняя Набережная, 14, Иркутск, Иркутская обл., 664011")
        office = Office("301")
        office.save()
        office_building.offices.add(office)
        office_building.save()