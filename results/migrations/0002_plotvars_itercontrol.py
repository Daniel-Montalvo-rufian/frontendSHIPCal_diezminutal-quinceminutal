# Generated by Django 3.0.3 on 2020-09-24 19:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='plotvars',
            name='itercontrol',
            field=models.CharField(default='paso_10min', max_length=35, verbose_name='Control of step resolution'),
            preserve_default=False,
        ),
    ]
