from django import forms

from app_jumanji.models import Application, Company, Vacancy


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = '__all__'
