# Generated by Django 2.2.5 on 2020-04-16 00:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0050_unidadescriticas_aprovado'),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='instalaciones',
            field=models.ManyToManyField(blank=True, to='facilities.Instalacion'),
        ),
    ]
