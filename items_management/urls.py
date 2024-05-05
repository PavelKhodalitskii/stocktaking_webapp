from .views import InvenoryItemsAPIView, StocktalkingListAPIView, ReportItemsApiView, ItemsListView, ItemDetailView

from django.urls import path


urlpatterns = [
    path('api/v1/items_list/', InvenoryItemsAPIView.as_view()),
    path('api/v1/stocktalking_list/', StocktalkingListAPIView.as_view()),
    path('api/v1/report_items/<int:report_id>', ReportItemsApiView.as_view()),
    path('<slug:officebuilding_slug>/items_list/', ItemsListView.as_view(), name="items_list"),
    path('<slug:officebuilding_slug>/items_list/<slug:item_slug>/', ItemDetailView.as_view(), name="item_detail")
]

