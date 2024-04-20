from django.urls import path
from django.contrib.auth.views import LogoutView

# from .views import 
from .views import user_login, logout_user, LoginUser

urlpatterns = [
    # path('login/', user_login, name='login'),
    path('login/', LoginUser.as_view(), name='login'),
    path('logout/', logout_user, name='logout')
]

