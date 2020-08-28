import operator
from functools import reduce

from django.db.models import Q
from django.http import HttpResponseNotFound, HttpResponseServerError, HttpResponse
from django.shortcuts import render, Http404
from django.views import View
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView

from app_jumanji.models import Specialty, Company, Vacancy, Resume

from jumanji.forms import ApplicationForm, CompanyForm, VacancyForm, ResumeForm, SignUpForm


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
            return HttpResponse('0 вакансий')
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
            return render(request, 'sent.html')
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
        companyform = CompanyForm(request.POST, request.FILES)
        user_id = request.user.id
        company = Company.objects.filter(owner_id=user_id).first()
        if companyform.is_valid():
            if not company:
                company = companyform.save(commit=False)
                company.owner = request.user
                company.save()
            Company.objects.filter(id=company.id).update(
                name=companyform.cleaned_data['name'],
                location=companyform.cleaned_data['location'],
                description=companyform.cleaned_data['description'],
                employee_count=companyform.cleaned_data['employee_count'],
                logo=companyform.cleaned_data['logo']
            )
        print(companyform.errors)
        context = {
            'companyform': companyform
        }
        return render(request, 'company-edit.html', context=context)


class MyCompanyVacanciesView(View):
    def get(self, request):
        user_id = request.user.id
        company = Company.objects.filter(owner_id=user_id).first()
        my_vacancies = company.vacancies.all()

        context = {
            'my_vacancies': my_vacancies,
        }
        return render(request, 'mycompany-vacancies.html', context=context)


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
        vacancyform = VacancyForm(request.POST)
        if vacancyform.is_valid():
            Vacancy.objects.filter(id=vacancy_id).update(
                title=vacancyform.cleaned_data['title'],
                specialty=vacancyform.cleaned_data['specialty'],
                salary_min=vacancyform.cleaned_data['salary_min'],
                salary_max=vacancyform.cleaned_data['salary_max'],
                skills=vacancyform.cleaned_data['skills'],
                description=vacancyform.cleaned_data['description'],
                published_at=vacancyform.cleaned_data['published_at']
            )
        # print(vacancyform.errors)
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
        if vacancyform.is_valid():
            vacancyform.save()
        # print(vacancyform.errors)
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
        resumeform = ResumeForm(request.POST)
        user_id = request.user.id
        resume = Resume.objects.filter(user_id=user_id).first()
        if resumeform.is_valid():
            if not resume:
                resume = resumeform.save(commit=False)
                resume.user = request.user
                resume.save()
            Resume.objects.filter(id=resume.id).update(
                name=resumeform.cleaned_data['name'],
                surname=resumeform.cleaned_data['surname'],
                status=resumeform.cleaned_data['status'],
                salary=resumeform.cleaned_data['salary'],
                specialty=resumeform.cleaned_data['specialty'],
                grade=resumeform.cleaned_data['grade'],
                education=resumeform.cleaned_data['education'],
                experience=resumeform.cleaned_data['experience'],
                portfolio=resumeform.cleaned_data['portfolio']
            )
        print(resumeform.errors)
        context = {
            'resumeform': resumeform
        }
        return render(request, 'resume-edit.html', context=context)


class MySignupView(CreateView):
    form_class = SignUpForm
    success_url = '/'
    template_name = 'signup.html'


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'


def custom_handler404(request, exception):
    return HttpResponseNotFound("<h1>page not found</h1>")


def custom_handler500(request):
    return HttpResponseServerError("<h1>server error</h1>")
