from rest_framework import serializers
from account.models import CustomUser, Role, OfficeBuilding, Office

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
    office_building = serializers.SerializerMethodField('get_office_building')

    class Meta:
        model = CustomUser
        fields = ("id", "username", "first_name", "last_name", "is_superuser", "office_building", "slug")
    
    def get_office_building(self, obj):
        if obj.office_building:
            office_building = OfficeBuilding.objects.get(id=obj.office_building.id)
            return OfficeBuildingSerializer(office_building).data

