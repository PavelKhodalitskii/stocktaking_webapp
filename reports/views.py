from typing import Any
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from .models import StocktalkingReport, RelationItemsReports, Ivent
from .serizalizers import StocktalkingListSerizalizer, RelationItemsReportsSerizalizer
from .createreports import create_report
from items_management.permissions import IsOwner
from items_management.models import Status
from account.models import OfficeBuilding, CustomUser

def report_view(request):
    try:
        create_report()
        return render(request, 'reports/report_create_view.html')
    except:
        return HttpResponse("Something went wrong")  

class ReportsView(TemplateView):
    template_name = "reports/reports_view.html"

    def get_report_items(self):
        user = self.request.user
        try:
            report = StocktalkingReport.objects.get(author__id = user.id)
            items = RelationItemsReports.objects.all().filter(report__id = report.id)
        except:
            items = RelationItemsReports.objects.none()

        status_id = self.request.GET.get('status')
        if status_id:
            items = items.filter(status__id = status_id)

        responsible_person_id = self.request.GET.get('responsible_person')
        if responsible_person_id:
            items = items.filter(item__financially_responsible_person__id=responsible_person_id)

        approved_filter = self.request.GET.get('approved')
        if approved_filter:
            if approved_filter == "True":
                items = items.filter(approve=True)
            elif approved_filter == "False":
                items = items.filter(approve=False)

        valid_from_sort = self.request.GET.get('scan_time')
        if valid_from_sort == 'ascending':
            items = items.order_by('-last_scan_datetime')
        elif valid_from_sort == 'descending':
            items = items.order_by('last_scan_datetime')

        return items
    
    def get_reports(self):
        office_building_slug = self.kwargs['officebuilding_slug']
        try:
            reports = StocktalkingReport.objects.all().filter(author__office_building=OfficeBuilding.objects.get(slug=office_building_slug))
        except:
            reports = StocktalkingReport.objects.none()
        return reports


    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context['title'] = "Отчеты"

        office_building_slug = self.kwargs['officebuilding_slug']
        context['office_building_slug'] = office_building_slug

        context['office_buildings'] = OfficeBuilding.objects.all()
        context['statuses'] = Status.objects.all()
        context['users'] = CustomUser.objects.all().filter(office_building__slug = office_building_slug)
        context['items'] = self.get_report_items()
        context['reports'] = self.get_reports()
        context['ivent'] = Ivent.objects.last()
        return context

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
    post_fields_required = ['item', 'report']
    put_fields_forbidden = ['id', 'item', 'report']

    def validate_post_data(self, data):
        for field in self.post_fields_required:
            if not field in data.keys():
                return False

        return True
    
    def validate_put_data(self, data):
        for field in self.put_fields_forbidden:
            if field in data.keys():
                return False

        return True
    
    def get(self, request, item_id):
        object = RelationItemsReports.objects.get(id=item_id)
        if object:
            return Response({'item': RelationItemsReportsSerizalizer(object, many=False).data
                            })
        return Response({"status": "No object with such id"})
    
    def post(self, request, item_id):
        serializer = RelationItemsReportsSerizalizer(data=request.data)
        if serializer.is_valid() and self.validate_post_data(request.data):
            serializer.save()
            return Response({"status": "Item successfuly added to relation"})
        else:
            return Response({"status": "Wrong data provided"})
        
    def put(self, request, item_id):
        object = RelationItemsReports.objects.get(id = item_id)
        if self.validate_put_data(request.data):
            if object:
                serializer = RelationItemsReportsSerizalizer(object, data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({"status": "Item successfuly updated"})
                else:
                    return Response({"status": "Wrong data provided"})
            return Response({"status": "No object with such id"})
        return Response({"status": f"Forbidden fields change. Note: it's forbidden to change fields: {self.put_fields_forbidden}"})

class ApproveItemByQR(APIView):
    permission_classes = (IsAdminUser, IsOwner)
    put_fields_forbidden = ['id', 'item', 'report', 'status', 'note']
    put_fields_required = ['approve', 'datatime']

    def approve_data(self, data):
        for field in self.put_fields_required:
            if field not in data.keys():
                return False
        
        for field in self.put_fields_forbidden:
            if field in data.keys():
                return False
        return True

    def put(self, request, item_id):
        try:
            object = RelationItemsReports.objects.get(id=item_id)
            if self.approve_data(request.data):
                if object:
                    serializer = RelationItemsReportsSerizalizer(object, data=request.data)
                    if serializer.is_valid():
                        serializer.save()
                        return Response({"status": "Item successfuly updated"})
                    else:
                        return Response({"status": "Wrong data provided"})
            return Response({"status": "Forbidden fields change or lack of required. Note: it's forbidden to change fields excluding 'approve' and 'datetime'"})
        except:
            return Response({"status": "No object with such id"})