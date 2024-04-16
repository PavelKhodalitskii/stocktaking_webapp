from rest_framework import generics
from django.shortcuts import render
from django.http import HttpResponse

from .models import InventoryItems
from .serizalizers import InventoryItemsSerializer

class InvenoryItemsAPIView(generics.ListAPIView):
    queryset = InventoryItems.objects.all()
    serializer_class = InventoryItemsSerializer
    pass

# Create your views here.
def main_view():
    return HttpResponse()