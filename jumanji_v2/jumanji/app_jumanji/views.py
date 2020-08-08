from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.shortcuts import render, Http404
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView


from app_jumanji.models import Specialty, Company, Vacancy

from jumanji.forms import ApplicationForm, CompanyForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'specialties': Specialty.objects.all(),
            'companies': Company.objects.all()
        }
        return render(request, 'base.html', context=context)


class VacanciesView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'vacancies': Vacancy.objects.all()
        }
        return render(request, 'vacancies.html', context=context)


class VacanciesSpecialtiesView(View):
    def get(self, request, code):
        specialty = Vacancy.objects.filter(specialty__code=code).first()
        if not specialty:
            raise Http404
        context = {
            'specialty': specialty,
            'vacancies': Vacancy.objects.all()
        }
        return render(request, 'vacancies.html', context=context)


class CompaniesView(View):
    def get(self, request, id):
        company = Company.objects.filter(id=id).first()
        vacancies = Vacancy.objects.filter(company__name=company.name).all()
        if not company:
            raise Http404
        context = {
            'company': company,
            'vacancies': vacancies
        }
        return render(request, 'company.html', context=context)


class VacancyView(View):
    def get(self, request, id):
        vacancy = Vacancy.objects.filter(id=id).first()
        if not vacancy:
            raise Http404
        applicationform = ApplicationForm()
        context = {
            'vacancy': vacancy,
            'applicationform': applicationform
        }
        return render(request, 'vacancy.html', context=context)

    def post(self, request):
        applicationform = ApplicationForm()
        if applicationform.is_valid():
            applicationform.save
            return HttpResponse('отклик отправлен')
        context = {
            'applicationform': applicationform
        }
        return render(request, 'vacancy.html', context=context)

class SendRequestView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'sendrequest.html')

    def post(self, request, *args, **kwargs):
        applicationform = ApplicationForm(request.POST)
        if applicationform.is_valid():
            applicationform.save()
            return HttpResponse('<h2>отклик отправлен</h2>')
        return render(request, 'sendrequest.html')

class CompanyCreateView(View):
    def get(self, request, vacancy_id):
        applicationform = ApplicationForm()
        context = {
            'vacancy_id': vacancy_id,
            'applicationform': applicationform
        }
        return render(request, 'company-create.html', context=context)


class MyCompanyView(View):
    def get(self, request):
        user_id = request.user.id
        company = Company.objects.filter(owner_id=user_id).first()
        if not company:
            return render(request, 'company-create.html')
        companyform = CompanyForm()
        context = {
            'companyform': companyform,
            'user_id': user_id,
            'company': company
        }
        return render(request, 'company-edit.html', context=context)


class MyCompanyVacanciesView(View):
    def get(self, request):
        context = {
            'vacancies': Vacancy.objects.all()
        }
        return render(request, 'vacancies.html', context=context)


class MyCompanyVacancyView(View):
    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        if not vacancy:
            raise Http404
        context = {
            'vacancy': vacancy
        }
        return render(request, 'vacancy.html', context=context)


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = '/'
    template_name = 'signup.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


def custom_handler404(request, exception):
    return HttpResponseNotFound("<h1>page not found</h1>")


def custom_handler500(request):
    return HttpResponseServerError("<h1>server error</h1>")
