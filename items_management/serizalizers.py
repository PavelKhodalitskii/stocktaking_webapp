from rest_framework import serializers

from account.models import Office, CustomUser
from account.serializers import OfficeSerializer, CustomUserSerializer
from .models import InventoryItems

#Items managemetn serializers
class InventoryItemsSerializer(serializers.ModelSerializer):
    office = serializers.SerializerMethodField('get_office')
    financially_responsible_person = serializers.SerializerMethodField('get_responsible_person_info')

    class Meta:
        model = InventoryItems
        fields = ('id', 'item_number', 'slug', 'name', 'office', 'value', 'amount', 'financially_responsible_person')

    def get_office(self, obj):
        if obj.office:
            office = Office.objects.get(id=obj.office.id)
            return OfficeSerializer(office).data
        
    def get_responsible_person_info(self, obj):
        if obj.financially_responsible_person:
            user = CustomUser.objects.get(id=obj.financially_responsible_person.id)
            return CustomUserSerializer(user).data
        
