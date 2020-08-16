from enum import Enum

from django.db import models
from django.contrib.auth.models import User

from jumanji.settings import MEDIA_SPECIALITY_IMAGE_DIR, MEDIA_COMPANY_IMAGE_DIR

from app_jumanji.data import WorkStatusChoices, SpecialtyChoices, GradeChoices, EducationChoices


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=MEDIA_COMPANY_IMAGE_DIR, default=None, null=True)
    description = models.CharField(max_length=200)
    employee_count = models.IntegerField()
    owner = models.ForeignKey(User, related_name='companies', on_delete=models.CASCADE)


class Specialty(models.Model):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    picture = models.ImageField(upload_to=MEDIA_SPECIALITY_IMAGE_DIR)


class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    specialty = models.ForeignKey(Specialty, related_name='vacancies', on_delete=models.CASCADE, default=None, null=True)
    company = models.ForeignKey(Company, related_name='vacancies', on_delete=models.CASCADE, default=None, null=True)
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


class Resume(models.Model):
    user = models.ForeignKey(User, related_name='resume', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=WorkStatusChoices)
    salary = models.FloatField()
    specialty = models.CharField(max_length=100, choices=SpecialtyChoices)
    grade = models.CharField(max_length=100, choices=GradeChoices)
    education = models.CharField(max_length=100, choices=EducationChoices)
    experience = models.CharField(max_length=500)
    portfolio = models.CharField(max_length=500)
