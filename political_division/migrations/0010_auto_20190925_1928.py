# Generated by Django 2.2.5 on 2019-09-25 19:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('political_division', '0009_auto_20190925_1847'),
    ]

    operations = [
        migrations.AddField(
            model_name='distrito',
            name='provincia',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='political_division.Provincia'),
        ),
        migrations.AlterField(
            model_name='distrito',
            name='region',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='political_division.Region'),
        ),
    ]
