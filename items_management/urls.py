from .views import InvenoryItemsAPIView

from django.urls import path


urlpatterns = [
    path('api/items_list/', InvenoryItemsAPIView.as_view())
]