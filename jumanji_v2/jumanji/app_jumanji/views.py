from django.http import HttpResponseNotFound, HttpResponseServerError
from django.shortcuts import render, Http404
from django.views import View

from app_jumanji.models import Specialty, Company, Vacancy


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
        context = {
            'vacancy': vacancy
        }
        return render(request, 'vacancy.html', context=context)

class CompanyCreateView(View):
    def get(self, request, vacancy_id):
        return render(request, 'company-create.html')


class MyCompanyView(View):
    def get(self, request):
        return render(request, 'company-edit.html')


class MyCompanyVacanciesView(View):
    def get(self, request):
        return render(request, 'vacancies.html')


class MyCompanyVacancyView(View):
    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        if not vacancy:
            raise Http404
        context = {
            'vacancy': vacancy
        }
        return render(request, 'vacancy.html', context=context)


def custom_handler404(request, exception):
    return HttpResponseNotFound("<h1>page not found</h1>")


def custom_handler500(request):
    return HttpResponseServerError("<h1>server error</h1>")
