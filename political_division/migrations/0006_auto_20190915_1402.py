# Generated by Django 2.2.5 on 2019-09-15 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('political_division', '0005_poblado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='corregimiento',
            name='cod_corr',
            field=models.CharField(max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='distrito',
            name='cod_dist',
            field=models.CharField(max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='poblado',
            name='cod_pob',
            field=models.CharField(max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='provincia',
            name='cod_prov',
            field=models.CharField(max_length=2, unique=True),
        ),
        migrations.AlterField(
            model_name='region',
            name='cod_reg',
            field=models.CharField(max_length=2, unique=True),
        ),
    ]
