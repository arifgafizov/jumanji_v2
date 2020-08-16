from django import forms
from django.forms import Select

from app_jumanji.models import Application, Company, Vacancy


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['owner', 'logo']


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        exclude = ['company']
        widgets = {'specialty': Select}
