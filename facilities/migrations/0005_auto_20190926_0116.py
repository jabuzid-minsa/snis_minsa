# Generated by Django 2.2.5 on 2019-09-26 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0004_instalacion_cod_inst'),
    ]

    operations = [
        migrations.AddField(
            model_name='instalacion',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='instalacion',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]
