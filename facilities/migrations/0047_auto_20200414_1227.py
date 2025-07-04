# Generated by Django 2.2.5 on 2020-04-14 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0046_remove_unidadescriticas_hospitalizados'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidadescriticas',
            name='camas_covid_sala',
            field=models.IntegerField(blank=True, help_text='Camas ocupadas por pacientes con COVID-19 en sala (incluir sospechosos y confirmados; no incluir camas de UCI o semiintensivo)', null=True, verbose_name='Camas COVID-19 en sala'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='camas_otro_sala',
            field=models.IntegerField(blank=True, help_text='Camas ocupadas por otras causas en sala (no incluir camas de UCI o semiintensivo)', null=True, verbose_name='Camas otras causas en sala'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='camas_sala',
            field=models.IntegerField(blank=True, help_text='Total de camas en sala (no incluir camas de UCI o semiintensivo, estén o no ocupadas)', null=True, verbose_name='Camas en sala'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='cirujanos',
            field=models.IntegerField(blank=True, null=True, verbose_name='Médicos Cirujanos'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='cirujanos_dispo',
            field=models.IntegerField(blank=True, null=True, verbose_name='Disponibles'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='terapistas_resp',
            field=models.IntegerField(blank=True, null=True, verbose_name='Terapistas Respiratorios'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='terapistas_resp_dispo',
            field=models.IntegerField(blank=True, null=True, verbose_name='Disponibles'),
        ),
    ]
