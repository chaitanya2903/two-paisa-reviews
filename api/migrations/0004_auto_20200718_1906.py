# Generated by Django 3.0.8 on 2020-07-18 13:36

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20200717_1358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='avg_rating',
            field=models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)]),
        ),
        migrations.AlterField(
            model_name='movie',
            name='num_ratings',
            field=models.IntegerField(),
        ),
    ]
