# Generated by Django 3.0.3 on 2020-10-08 18:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('simforms', '0003_auto_20201007_1846'),
    ]

    operations = [
        migrations.AddField(
            model_name='simulation',
            name='annual',
            field=models.CharField(choices=[('yes', 'Yes'), ('no', 'No')], default='yes', max_length=3, verbose_name='In case you want to simulate in a full year'),
            preserve_default=False,
        ),
    ]
