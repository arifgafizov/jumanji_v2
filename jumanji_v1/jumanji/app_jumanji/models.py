from django.db import models


class Company(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=50)
    logo = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    employee_count = models.IntegerField()


class Specialty(models.Model):
    code = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    picture = models.CharField(max_length=200)


class Vacancy(models.Model):
    title = models.CharField(max_length=50)
    specialty = models.ForeignKey(Specialty, related_name='vacancies', on_delete=models.CASCADE)
    company = models.ForeignKey(Company, related_name='vacancies', on_delete=models.CASCADE)
    skills = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    salary_min = models.FloatField()
    salary_max = models.FloatField()
    published_at = models.DateField()
