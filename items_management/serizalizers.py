from rest_framework import serializers

from .models import InventoryItems
from reports.models import StocktalkingReport

class InventoryItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryItems
        fields = ('id', 'item_number', 'name', 'value', 'amount')


class StocktalkingListSerizalizer(serializers.ModelSerializer):
    class Meta:
        model = StocktalkingReport
        fields = ('author', 'ivent', 'type', 'items', 'slug', 'note')