from django import forms
from django.forms import Select
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app_jumanji.models import Application, Company, Vacancy, Resume


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['owner']


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ['company']
        widgets = {'specialty': Select}


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        exclude = ['user']


class SignUpForm(UserCreationForm):
  class Meta:
    model = User
    fields = ('username', 'first_name', 'last_name')
