# Generated by Django 2.2.5 on 2020-03-31 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0036_auto_20200331_1408'),
    ]

    operations = [
        migrations.AddField(
            model_name='instalacion',
            name='observaciones',
            field=models.TextField(blank=True, null=True, verbose_name='Observaciones'),
        ),
    ]
