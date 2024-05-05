from typing import Any

from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import InventoryItems, ItemType
from account.models import CustomUser, Office
from reports.models import StocktalkingReport, RelationItemsReports

from .serizalizers import InventoryItemsSerializer, StocktalkingListSerizalizer, RelationItemsReportsSerizalizer
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

class StocktalkingListAPIView(APIView):
    permission_classes = (IsAdminUser, IsOwner)

    def get(self, request):
        report = StocktalkingReport.objects.get(author__id = request.user.id)
        items = report.items.all()
        rel_info = RelationItemsReports.objects.all().filter(report=report)

        return Response({'report': StocktalkingListSerizalizer(report, many=False).data,
                         'relations_info': RelationItemsReportsSerizalizer(rel_info, many=True).data
                         })

class ReportItemsApiView(APIView):
    permission_classes = (IsAdminUser, IsOwner)
    serializer_class = RelationItemsReportsSerizalizer

    def validate_data(self, data):
        fields_required = ['datatime', 'item', 'report']

        for field in fields_required:
            if not field in data.keys():
                return False

        return True

    def get(self, request, report_id):
        reports = RelationItemsReports.objects.all().filter(report__id = report_id)
        return Response({'items': RelationItemsReportsSerizalizer(reports, many=True).data
                         })
    
    def post(self, request, report_id):
        serializer = RelationItemsReportsSerizalizer(data=request.data)
        if serializer.is_valid() and self.validate_data(request.data):
            serializer.save()
            return Response({"status": "Item successfuly added to relation"})
        else:
            return Response({"status": "Wrong data provided"})
        
    def put(self, request, report_id):
        serializer = RelationItemsReportsSerizalizer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Item successfuly updated"})
        else:
            return Response({"status": "Wrong data provided"})

# Create your views here.
def main_view():
    return HttpResponse()