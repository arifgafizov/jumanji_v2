from django.db import models
from django.contrib.auth.models import User

from jumanji.settings import MEDIA_SPECIALITY_IMAGE_DIR, MEDIA_COMPANY_IMAGE_DIR


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR)
    description = models.CharField(max_length=200)
    employee_count = models.IntegerField()
    owner = models.ForeignKey(User, related_name='companies', on_delete=models.CASCADE)


class Specialty(models.Model):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)


class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    specialty = models.ForeignKey(Specialty, related_name='vacancies', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='vacancies', on_delete=models.CASCADE)
    skills = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.DateField()


class Application(models.Model):
    written_username = models.CharField(max_length=100)
    written_phone = models.IntegerField()
    written_cover_letter = models.CharField(max_length=300)
    vacancy = models.ForeignKey(Vacancy, related_name='applications', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='applications', on_delete=models.CASCADE)
