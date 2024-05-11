from rest_framework import serializers

from account.models import Office
from account.serializers import OfficeSerializer
from .models import InventoryItems

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