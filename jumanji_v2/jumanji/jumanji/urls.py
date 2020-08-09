"""jumanji URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LogoutView

from app_jumanji.views import IndexView, VacanciesView, CompaniesView, VacancyView, VacanciesSpecialtiesView, \
    custom_handler404, custom_handler500, MyCompanyView, MyCompanyVacanciesView, MyCompanyVacancyView, \
    MySignupView, MyLoginView, SendRequestView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view()),
    path('vacancies/', VacanciesView.as_view(), name='vacancies'),
    path('vacancies/<str:code>/', VacanciesSpecialtiesView.as_view(), name='specialties'),
    path('companies/<int:id>/', CompaniesView.as_view(), name='companies'),
    path('vacancies/<int:id>', VacancyView.as_view(), name='vacancy'),
    path('vacancies/<int:vacancy_id>/send', SendRequestView.as_view(), name='send_request'),
    path('mycompany', MyCompanyView.as_view(), name='mycompany'),
    path('mycompany/vacancies', MyCompanyVacanciesView.as_view(), name='mycompany_vacancies'),
    path('mycompany/vacancies/<int:vacancy_id>', MyCompanyVacancyView.as_view(), name='mycompany_vacancy'),
    path('login', MyLoginView.as_view()),
    path('logout', LogoutView.as_view()),
    path('signup', MySignupView.as_view()),
]

handler404 = custom_handler404
handler500 = custom_handler500

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
