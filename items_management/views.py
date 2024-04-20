from typing import Any
from rest_framework import generics
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import InventoryItems
from .serizalizers import InventoryItemsSerializer

class ItemsListView(LoginRequiredMixin, ListView):
    model = InventoryItems
    template_name = 'items_management/items_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "Объекты инвентаризации"
        return context

    def get_queryset(self) -> generics.QuerySet[Any]:
        queryset = super().get_queryset()
        return queryset

class InvenoryItemsAPIView(generics.ListAPIView):
    queryset = InventoryItems.objects.all()
    serializer_class = InventoryItemsSerializer
    pass

# Create your views here.
def main_view():
    return HttpResponse()