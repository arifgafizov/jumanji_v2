# Generated by Django 3.0.8 on 2020-08-15 19:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_jumanji', '0005_auto_20200815_2210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vacancy',
            name='company',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE,
                                    related_name='vacancies', to='app_jumanji.Company'),
        ),
    ]
