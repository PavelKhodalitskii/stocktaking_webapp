from django.db.models.query import QuerySet
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView
from django.db.models import Q

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from .forms import LoginForm, RegisterUserForm
from .models import OfficeBuilding, Office, CustomUser
from .serializers import OfficeSerializer, CustomUserSerializer
from items_management.permissions import IsOwner

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

class UserRetriveAPIView(APIView):
    permission_classes = (IsAdminUser, IsOwner)

    def get(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        return Response({f"user {user_id}": CustomUserSerializer(user).data})
    
class UsersListView(ListView):
    model = CustomUser
    template_name = 'account/users_list.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "Пользователи"
        
        context['office_buildings'] = OfficeBuilding.objects.all()
        context['superadmin'] = CustomUser.objects.get(is_superuser=True)

        office_building_slug = self.kwargs['officebuilding_slug']
        context['office_building_slug'] = office_building_slug
        try:
            context['local_admin'] = CustomUser.objects.get(Q(is_admin=True) & Q(office_building__slug = office_building_slug))
        except:
            context['local_admin'] = ''
        context['stocktalking_responsibles'] = CustomUser.objects.all().filter(is_stocktalking_responsible = True)
        return context
    
    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.exclude(id=self.request.user.id)

        office_building_slug = self.kwargs['officebuilding_slug']
        queryset = queryset.filter(office_building__slug=office_building_slug)
        queryset = queryset.exclude(is_stocktalking_responsible = True)
        return queryset