from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


from .forms import LoginForm


class LoginUser(auth_views.LoginView):
    form_class = LoginForm
    template_name = 'login.html'

    def get_success_url(self) -> str:
        return reverse_lazy('items_list')

def logout_user(request):
    logout(request)
    return redirect('login')

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