from typing import Any

from rest_framework import generics

from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import InventoryItems, ItemType
from account.models import CustomUser, Office

from .serizalizers import InventoryItemsSerializer
from .permissions import IsOwner


class ItemsListView(LoginRequiredMixin, ListView):
    model = InventoryItems
    template_name = 'items_management/items_list.html'
    context_object_name = 'items'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "Объекты инвентаризации"
        
        office_building_slug = self.kwargs['officebuilding_slug']

        context['offices'] = Office.objects.all().filter(office_building__slug=office_building_slug)
        context['types'] = ItemType.objects.all()
        context['users'] = CustomUser.objects.all().filter(office_building__slug=office_building_slug)
        context['office_building_slug'] = office_building_slug
        return context

    def get_queryset(self) -> generics.QuerySet[Any]:
        office_building_slug = self.kwargs['officebuilding_slug']
        queryset = super().get_queryset()
        queryset = queryset.order_by('-valid_from')
        queryset = queryset.filter(office__office_building__slug=office_building_slug)

        office_id = self.request.GET.get('office')
        if office_id:
            queryset = queryset.filter(office__id=office_id)

        type_id = self.request.GET.get('type')
        if type_id:
            queryset = queryset.filter(type__id=type_id)

        responsible_person_id = self.request.GET.get('responsible_person')
        if responsible_person_id:
            queryset = queryset.filter(financially_responsible_person__id=responsible_person_id)    

        value_sort = self.request.GET.get('value_sort')
        if value_sort == 'expensive':
            queryset = queryset.order_by('-value')
        elif value_sort == 'cheap':
            queryset = queryset.order_by('value')

        assessed_value_sort = self.request.GET.get('assessed_value_sort')
        if assessed_value_sort == 'expensive':
            queryset = queryset.order_by('-assessed_value')
        elif assessed_value_sort == 'cheap':
            queryset = queryset.order_by('assessed_value')

        amount_sort = self.request.GET.get('amount_sort')
        if amount_sort == 'ascending':
            queryset = queryset.order_by('-amount')
        elif amount_sort == 'descending':
            queryset = queryset.order_by('amount')

        valid_from_sort = self.request.GET.get('valid_from_sort')
        if valid_from_sort == 'ascending':
            queryset = queryset.order_by('-valid_from')
        elif valid_from_sort == 'descending':
            queryset = queryset.order_by('valid_from')

        return queryset

class ItemDetailView(DetailView):
    template_name = 'items_management/item_detail.html'
    model = InventoryItems
    slug_url_kwarg = 'item_slug'
    context_object_name = 'item'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)

        office_building_slug = self.kwargs['officebuilding_slug']
        context['office_building_slug'] = office_building_slug
        return context

class InvenoryItemsAPIView(generics.ListAPIView):
    queryset = InventoryItems.objects.all()
    serializer_class = InventoryItemsSerializer