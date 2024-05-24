from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from account.models import CustomUser, OfficeBuilding
from items_management.models import ItemType

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Имя'}))
    last_name = forms.CharField(label='Фамилия', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Фамилия'}))
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Логин'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Пароль'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'Повторите пароль'}))
    slug = forms.SlugField(label='Слаг', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Слаг'}))
    office_building = forms.ModelChoiceField(OfficeBuilding.objects.all())
    type = forms.ModelChoiceField(ItemType.objects.all())
    is_admin = forms.BooleanField(label='Администратор')
    stocktalking_responsible = forms.BooleanField(label='Ответсвенный за инвентаризацию')


    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'username', 'password1', 'password2', 
                  'slug', 'office_building', 'type', 'is_admin', 'stocktalking_responsible')