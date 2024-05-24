from django.urls import path

from .views import StocktalkingListAPIView, ReportItemsApiView, ApproveItemByQR, ReportsView, report_view

urlpatterns = [
    path('<slug:officebuilding_slug>/reports/', ReportsView.as_view(), name='reports'),
    path('create_report/', report_view, name='create_report'),
    path('api/v1/stocktalking_list/', StocktalkingListAPIView.as_view()),
    path('api/v1/report_items/<int:item_id>', ReportItemsApiView.as_view(), name='report_item'),
    # path('api/v1/approve_item/<int:item_id>', ApproveItemByQR.as_view(), name="approve_item")
]