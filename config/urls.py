"""
URL configuration for inventory_checking project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import redirect
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

from .utils import debug_prepare
from account.models import OfficeBuilding


def root_redirect(request):
    debug_prepare()
    if request.user.is_authenticated:
        return redirect('items_list', OfficeBuilding.objects.get(id=1).slug)
    return redirect('site_login')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('inventory_items/', include('items_management.urls'), name='api'),
    path('account/', include('account.urls'), name='account'),
    path('reports/', include('reports.urls'), name='reports'),
    path('', root_redirect)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)