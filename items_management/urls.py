from .views import InvenoryItemsAPIView, ItemsListView, ItemDetailView, InventoryItemRetriveAPIView, StatusesListApiView

from django.urls import path


urlpatterns = [
    path('api/v1/statuses/', StatusesListApiView.as_view()),
    path('api/v1/item/<int:item_id>', InventoryItemRetriveAPIView.as_view()),
    path('api/v1/items_list/', InvenoryItemsAPIView.as_view()),
    path('api/v1/statuses/', StatusesListApiView.as_view()),
    path('<slug:officebuilding_slug>/items_list/', ItemsListView.as_view(), name="items_list"),
    path('<slug:officebuilding_slug>/items_list/<slug:item_slug>/', ItemDetailView.as_view(), name="item_detail")
]

