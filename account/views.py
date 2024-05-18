from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .forms import LoginForm, RegisterUserForm
from .models import OfficeBuilding, Office
from .serializers import OfficeSerializer


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'account/register.html'
    success_url = reverse_lazy('site_login')


class LoginUser(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'account/login.html'

    def get_success_url(self) -> str:
        return reverse_lazy('items_list', kwargs={'officebuilding_slug': OfficeBuilding.objects.get(pk=1).slug})

def logout_user(request):
    logout(request)
    return redirect('site_login')

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            user = authenticate(request, username=cleaned_data['username'],
                                password=cleaned_data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

class OfficeListApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, office_building_id):
        offices = Office.objects.all().filter(office_building=office_building_id)
        return Response({'offices': OfficeSerializer(offices, many=True).data})

