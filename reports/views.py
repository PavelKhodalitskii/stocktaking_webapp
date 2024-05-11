from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser

from reports.models import StocktalkingReport, RelationItemsReports
from .serizalizers import StocktalkingListSerizalizer, RelationItemsReportsSerizalizer
from items_management.permissions import IsOwner

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
    post_fields_required = ['datatime', 'item', 'report']
    put_fields_forbidden = ['id', 'item', 'report']

    def validate_post_data(self, data):
        self.post_fields_required = ['datatime', 'item', 'report']

        for field in self.post_fields_required:
            if not field in data.keys():
                return False

        return True
    
    def validate_put_data(self, data):
        self.put_fields_forbidden = ['id', 'item', 'report']

        for field in self.put_fields_forbidden:
            if not field in data.keys():
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