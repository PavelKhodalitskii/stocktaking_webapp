from .views import InvenoryItemsAPIView, ItemsListView

from django.urls import path


urlpatterns = [
    path('api/items_list/', InvenoryItemsAPIView.as_view()),
    path('items_list/', ItemsListView.as_view(), name="items_list")
]