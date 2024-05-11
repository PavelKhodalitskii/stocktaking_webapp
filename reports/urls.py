from django.urls import path

from .views import StocktalkingListAPIView, ReportItemsApiView, report_view

urlpatterns = [
    path('report/', report_view, name='report')
    path('api/v1/stocktalking_list/', StocktalkingListAPIView.as_view()),
    path('api/v1/report_items/<int:item_id>', ReportItemsApiView.as_view()),
]