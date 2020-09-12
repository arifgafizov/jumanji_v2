import operator
from functools import reduce
from datetime import datetime

from django.contrib.auth import authenticate, login
from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.shortcuts import render, Http404
from django.views import View
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User

from app_jumanji.models import Specialty, Company, Vacancy, Resume, Application
from app_jumanji.forms import ApplicationForm, CompanyForm, VacancyForm, ResumeForm, SignUpForm, UserUpdateForm


class IndexView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'specialties': Specialty.objects.all(),
            'companies': Company.objects.all()
        }
        return render(request, 'index.html', context=context)


class AboutView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html')


class VacanciesView(ListView):
    model = Vacancy
    template_name = 'vacancies.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancies_all_count'] = self.get_queryset().count
        return context


class VacanciesSpecialtiesView(View):
    def get(self, request, code):
        specialty = Specialty.objects.filter(code=code).first()
        vacancies = Vacancy.objects.filter(specialty=specialty.id).all()
        if not specialty:
            raise Http404
        context = {
            'specialty': specialty,
            'vacancies': vacancies
        }
        return render(request, 'vacancies-specialties.html', context=context)


class CompanyView(View):
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


class CompaniesView(ListView):
    model = Company
    template_name = 'companies.html'
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies_all_count'] = self.get_queryset().count
        return context


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


class SendRequestView(View):
    def get(self, request, vacancy_id, *args, **kwargs):
        return render(request, 'sendrequest.html')

    def post(self, request, vacancy_id, *args, **kwargs):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        applicationform = ApplicationForm(request.POST)
        if applicationform.is_valid():
            application = applicationform.save(commit=False)
            application.user = request.user
            application.vacancy = vacancy
            application.save()
            return render(request, 'sent.html')
        return render(request, 'sendrequest.html')


class CompanyCreateView(View):
    def get(self, request, *args, **kwargs):
        companyform = CompanyForm()
        context = {
            'companyform': companyform,
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

    def post(self, request):
        company = request.user.companies.first()
        companyform = CompanyForm(request.POST, request.FILES, instance=company)
        if companyform.is_valid():
            if not company:
                company = companyform.save(commit=False)
                company.owner = request.user
                company.save()
            companyform.save()
        context = {
            'companyform': companyform
        }
        return render(request, 'company-edit.html', context=context)


class MyCompanyVacanciesView(View):
    def get(self, request):
        if request.user.is_authenticated:
            user_id = request.user.id
            company = Company.objects.filter(owner_id=user_id).first()
            if company:
                my_vacancies = company.vacancies.all()
                context = {'my_vacancies': my_vacancies,}
                return render(request, 'mycompany-vacancies.html', context=context)
            else:
                return render(request, 'company-create.html')
        return render(request, 'login.html')


class MyCompanyVacancyView(View):
    def get(self, request, vacancy_id):
        vacancy = Vacancy.objects.filter(id=vacancy_id).first()
        if not vacancy:
            raise Http404
        vacancyform = VacancyForm()
        specialties = Specialty.objects.all()
        applications = vacancy.applications.all
        context = {
            'vacancy': vacancy,
            'vacancyform': vacancyform,
            'specialties': specialties,
            'applications': applications
        }
        return render(request, 'mycompany-vacancy.html', context=context)

    def post(self, request, vacancy_id, *args, **kwargs):
        vacancy = Vacancy.objects.get(id=vacancy_id)
        vacancyform = VacancyForm(request.POST, instance=vacancy)
        current_date = datetime.now().date()
        if vacancyform.is_valid():
            vacancy = vacancyform.save(commit=False)
            vacancy.published_at = current_date
            vacancy.save()
        context = {
            'vacancyform': vacancyform,
        }
        return render(request, 'mycompany-vacancy.html', context=context)


class MyCompanyVacancyAddView(View):
    def get(self, request):
        user_id = request.user.id
        company = Company.objects.filter(owner_id=user_id).first()
        vacancyform = VacancyForm()
        specialties = Specialty.objects.all()
        context = {
            'vacancyform': vacancyform,
            'specialties': specialties,
            'company': company
        }
        return render(request, 'mycompany-vacancy-add.html', context=context)

    def post(self, request, *args, **kwargs):
        vacancyform = VacancyForm(request.POST)
        company = request.user.companies.first()
        current_date = datetime.now().date()
        if vacancyform.is_valid():
            vacancy = vacancyform.save(commit=False)
            vacancy.company = company
            vacancy.published_at = current_date
            vacancy.save()
        context = {
            'vacancyform': vacancyform,
        }
        return render(request, 'mycompany-vacancy-add.html', context=context)


class SearchView(ListView):
    model = Vacancy
    template_name = 'search.html'
    paginate_by = 10
    ordering = ['-published_at']

    def get_queryset(self):
        result = super(SearchView, self).get_queryset()
        query = self.request.GET.get('s')

        if query:
            query_list = query.split()
            result = result.filter(
                reduce(operator.and_,
                       (Q(title__icontains=s) for s in query_list)) |
                reduce(operator.and_,
                       (Q(description__icontains=s) for s in query_list))  |
                reduce(operator.and_,
                       (Q(skills__icontains=s) for s in query_list))
            )
        return result


class MyResumeView(View):
    def get(self, request):
        userid = request.user.id
        resume = Resume.objects.filter(user_id=userid).first()
        if not resume:
            return render(request, 'resume-create.html')
        resumeform = ResumeForm()
        context = {
            'resumeform': resumeform,
            'userid': userid,
            'resume': resume,
         }
        return render(request, 'resume-edit.html', context=context)

    def post(self, request):
        user_id = request.user.id
        resume = Resume.objects.filter(user_id=user_id).first()
        resumeform = ResumeForm(request.POST, instance=resume)
        if resumeform.is_valid():
            if not resume:
                resume = resumeform.save(commit=False)
                resume.user = request.user
                resume.save()
            resumeform.save()
        context = {
            'resumeform': resumeform
        }
        return render(request, 'resume-edit.html', context=context)


class MyProfileView(View):
    def get(self, request, *args, **kwargs):
        profile_user = User.objects.get(pk=request.user.pk)
        context = {
            'user': profile_user
        }
        return render(request, 'profile.html', context=context)

    def post(self, request, *args, **kwargs):
        userupdateform = UserUpdateForm(request.POST, instance=request.user)
        if userupdateform.is_valid():
            userupdateform.save()
        context = {
            'userupdateform': userupdateform,
        }
        return render(request, 'profile.html', context=context)


class MySignupView(CreateView):
    form_class = SignUpForm
    success_url = '/'
    template_name = 'signup.html'

    def form_valid(self, form):
        valid = super(MySignupView, self).form_valid(form)
        username, password = form.cleaned_data.get('username'), form.cleaned_data.get('password1')
        new_user = authenticate(username=username, password=password)
        login(self.request, new_user)
        return valid


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


def custom_handler404(request, exception):
    return HttpResponseNotFound("<h1>page not found</h1>")


def custom_handler500(request):
    return HttpResponseServerError("<h1>server error</h1>")
