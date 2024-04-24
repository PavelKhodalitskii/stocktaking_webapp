from .views import InvenoryItemsAPIView, ItemsListView, ItemDetailView

from django.urls import path


urlpatterns = [
    path('api/items_list/', InvenoryItemsAPIView.as_view()),
    path('items_list/', ItemsListView.as_view(), name="items_list"),
    path('items_list/<slug:item_slug>/', ItemDetailView.as_view(), name="item_detail")
]