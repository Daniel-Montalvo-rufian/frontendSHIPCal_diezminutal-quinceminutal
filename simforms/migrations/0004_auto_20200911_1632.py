# Generated by Django 3.0.3 on 2020-09-11 14:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simforms', '0003_auto_20200911_1517'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='hourEND',
            field=models.TimeField(verbose_name='Ending time'),
        ),
        migrations.AlterField(
            model_name='simulation',
            name='hourINI',
            field=models.TimeField(verbose_name='Starting time'),
        ),
    ]