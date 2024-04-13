from rest_framework import serializers

from .models import InventoryItems

class InventoryItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItems
        fields = ('id', 'item_number', 'name', 'value', 'amount')
