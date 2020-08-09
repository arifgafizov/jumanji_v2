from django import forms


from app_jumanji.models import Application, Company


class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = '__all__'


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'
