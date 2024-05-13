from account.models import CustomUser, OfficeBuilding, Office
from items_management.models import InventoryItems, ItemType, Status
import random

def debug_prepare():
    print("Preparing for debug")

    # Создание суперользователя
    superuser = ''
    try: 
        superuser = CustomUser.objects.get(username="admin")
    except:
        superuser = CustomUser(username="admin", first_name="Админ", last_name="Админов", is_staff=True, is_superuser=True, is_active=True)
        superuser.set_password("admin")
        superuser.save()

    #Создание офиса
    office_building = ''
    try:
        office_building = OfficeBuilding.objects.get(pk=1)
    except:
        office_building = OfficeBuilding(slug='en_plus_digital', address="ул. Нижняя Набережная, 14, Иркутск, Иркутская обл., 664011")
        office_building.save()

    #Создание базового типа предмета
    item_type = ''
    try:
        item_type = ItemType.objects.get(pk=1)
    except:
        item_type = ItemType(name="Техника")
        item_type.save()

    #Создание дефолтного статуса
    status = ''
    try:
        status = Status.objects.get(pk=1)
    except:
        status = Status(name="В работе")
        status.save()

    create_offices(10)
    create_place_holder_items(20, 10)


def create_offices(amount):
    for i in range(amount):
        try:
            Office.objects.get(pk=i)
        except:
            office = Office(id=i, 
                            name=f"Помещение {i}", 
                            office_building=OfficeBuilding.objects.get(pk=1))
            office.save()

def create_place_holder_items(amount, offices_amount):
    for i in range(amount):
        try:
            InventoryItems.objects.get(id=i)
        except:
            new_item = InventoryItems(id=i, 
                                    item_number=i, 
                                    slug=f"placeholder_{i}", 
                                    name="Placeholder",
                                    office=Office.objects.get(id=random.randint(1, offices_amount)),
                                    type=ItemType.objects.get(pk=1),
                                    financially_responsible_person=CustomUser.objects.get(pk=1),
                                    status=Status.objects.get(pk=1)
                                    )
            new_item.save()