from django.urls import path, include, re_path
from django.contrib.auth.views import LogoutView

from .views import user_login, logout_user, LoginUser, OfficeListApiView, RegisterUser, UserRetriveAPIView

urlpatterns = [
    # path('login/', user_login, name='login'),
    path('login/', LoginUser.as_view(), name='site_login'),
    path('register/', RegisterUser.as_view(), name='site_register'),
    path('logout/', logout_user, name='site_logout'),
    # path('api/v1/auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/v1/offices/<int:office_building_id>', OfficeListApiView.as_view()),
    path('api/v1/user/<int:user_id>', UserRetriveAPIView.as_view())
]

