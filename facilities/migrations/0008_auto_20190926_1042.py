# Generated by Django 2.2.5 on 2019-09-26 10:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0007_auto_20190926_0949'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instalacion',
            name='cod_inst',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
