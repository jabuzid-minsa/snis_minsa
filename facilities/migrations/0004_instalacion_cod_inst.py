# Generated by Django 2.2.5 on 2019-09-25 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('facilities', '0003_auto_20190915_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='instalacion',
            name='cod_inst',
            field=models.CharField(blank=True, max_length=12, null=True, unique=True),
        ),
    ]
