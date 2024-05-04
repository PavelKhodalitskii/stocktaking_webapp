from rest_framework import serializers

from account.models import CustomUser, Role, OfficeBuilding, Office
from .models import InventoryItems
from reports.models import StocktalkingReport, RelationItemsReports



#Account serializers
class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"

class OfficeBuildingSerializer(serializers.ModelSerializer):
    class Meta:
        model = OfficeBuilding
        fields = "__all__"

class OfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Office
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer):
    role = serializers.SerializerMethodField('get_role')
    office_building = serializers.SerializerMethodField('get_office_building')

    class Meta:
        model = CustomUser
        fields = ("id", "username", "first_name", "last_name", "is_superuser", "role", "office_building", "slug")

    def get_role(self, obj):
        if obj.role:
            role = Role.objects.get(id=obj.role.id)
            return RoleSerializer(role).data
    
    def get_office_building(self, obj):
        if obj.office_building:
            office_building = OfficeBuilding.objects.get(id=obj.office_building.id)
            return OfficeBuildingSerializer(office_building).data


#Items managemetn serializers
class InventoryItemsSerializer(serializers.ModelSerializer):
    office = serializers.SerializerMethodField('get_office')

    class Meta:
        model = InventoryItems
        fields = ('id', 'item_number', 'slug', 'name', 'office', 'value', 'amount')

    def get_office(self, obj):
        if obj.office:
            office = Office.objects.get(id=obj.office.id)
            return OfficeSerializer(office).data
        

#Reports serializers
class StocktalkingListSerizalizer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField('get_author')
    items = serializers.SerializerMethodField('get_items')

    class Meta:
        model = StocktalkingReport
        fields = ('id', 'author', 'ivent', 'type', 'items', 'slug', 'note')


    def get_author(self, obj):
        author = CustomUser.objects.get(id=obj.author.id)
        return CustomUserSerializer(author).data
    
    def get_items(self, obj):
        items = obj.items.all()
        return InventoryItemsSerializer(items, many=True).data

class RelationItemsReportsSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = RelationItemsReports
        fields = "__all__"