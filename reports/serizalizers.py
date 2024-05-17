from rest_framework import serializers

from items_management.models import InventoryItems
from reports.models import StocktalkingReport, RelationItemsReports
from account.models import CustomUser
from account.serializers import CustomUserSerializer
from items_management.serizalizers import InventoryItemsSerializer

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
    item = serializers.SerializerMethodField('get_item')
    

    class Meta:
        model = RelationItemsReports
        fields = "__all__"

    def get_item(self, obj):
        if obj.item:
            item = InventoryItems.objects.get(id=obj.item.id)
            return InventoryItemsSerializer(item).data