# Generated by Django 3.0.3 on 2020-10-08 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0006_auto_20201008_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='plotvars',
            name='Q_drum',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plotvars',
            name='Q_prod_rec',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plotvars',
            name='Q_prod_steam',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plotvars',
            name='SD_energy',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plotvars',
            name='SD_max_energy',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plotvars',
            name='SD_min_energy',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='plotvars',
            name='step_sim',
            field=models.TextField(default=0, verbose_name='Simlation steps'),
            preserve_default=False,
        ),
    ]