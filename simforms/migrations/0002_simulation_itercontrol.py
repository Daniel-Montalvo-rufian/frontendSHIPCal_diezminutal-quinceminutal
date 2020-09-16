# Generated by Django 3.0.3 on 2020-09-11 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simforms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='itercontrol',
            field=models.CharField(choices=[('paso_10min', 'ten-minutes steps'), ('paso_15min', 'fifteen-minutes steps')], default='paso_10min', max_length=10, verbose_name='Step control'),
            preserve_default=False,
        ),
    ]
