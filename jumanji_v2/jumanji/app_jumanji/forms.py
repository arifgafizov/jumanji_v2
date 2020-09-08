from django import forms
from django.forms import Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app_jumanji.models import Application, Company, Vacancy, Resume


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ('written_username', 'written_phone', 'written_cover_letter')


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['owner']


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ['company', 'published_at']
        widgets = {'specialty': Select}


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ['user']


class SignUpForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput, label='Пароль')
    password2 = None
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
        labels = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }
        help_texts = {
            'username': 'Требование к логину. Не более 150 символов. И только буквы, цифры и символы @/./+/-/_.'
        }

