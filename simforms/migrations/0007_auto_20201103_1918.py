# Generated by Django 3.0.3 on 2020-11-03 18:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simforms', '0006_auto_20201103_1916'),
    ]

    operations = [
        migrations.AlterField(
            model_name='simulation',
            name='huso',
            field=models.FloatField(verbose_name='In case you have chosen to calculate solar time, write here the difference between the format of the TMY`s time and UTC'),
        ),
    ]