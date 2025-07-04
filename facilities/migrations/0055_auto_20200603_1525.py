# Generated by Django 2.2.5 on 2020-06-03 15:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0054_auto_20200504_1812'),
    ]

    operations = [
        migrations.AddField(
            model_name='unidadescriticas',
            name='pacientes_vma_fijo',
            field=models.IntegerField(blank=True, help_text='Pacientes con COVID-19 con VMA tipo fijo', null=True, verbose_name='Ventilador tipo fijo'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='pacientes_vma_sala_fijo',
            field=models.IntegerField(blank=True, help_text='Pacientes con COVID-19 con VMA en sala tipo fijo', null=True, verbose_name='Ventilador tipo fijo'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='pacientes_vma_sala_trans',
            field=models.IntegerField(blank=True, help_text='Pacientes con COVID-19 con VMA en sala tipo transporte', null=True, verbose_name='Ventilador tipo trasporte'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='pacientes_vma_trans',
            field=models.IntegerField(blank=True, help_text='Pacientes con COVID-19 con VMA tipo transorte', null=True, verbose_name='Ventilador tipo trasporte'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='vent_dispo_fijo',
            field=models.IntegerField(blank=True, help_text='Ventiladores disponibles tipo fijo', null=True, verbose_name='Ventilador tipo fijo'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='vent_dispo_trans',
            field=models.IntegerField(blank=True, help_text='Ventiladores disponibles tipo transporte', null=True, verbose_name='Ventilador tipo trasporte'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='vent_otro_fijo',
            field=models.IntegerField(blank=True, help_text='Ventiladores ocupados con otras patologías tipo fijo', null=True, verbose_name='Ventilador tipo fijo'),
        ),
        migrations.AddField(
            model_name='unidadescriticas',
            name='vent_otro_trans',
            field=models.IntegerField(blank=True, help_text='Ventiladores ocupados con otras patologías tipo transporte', null=True, verbose_name='Ventilador tipo trasporte'),
        ),
    ]
