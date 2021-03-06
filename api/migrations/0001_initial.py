# Generated by Django 3.0.8 on 2020-07-16 13:34

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django_mysql.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('movie_name', models.CharField(max_length=100, unique=True)),
                ('release_date', models.DateField(blank=True)),
                ('description', models.TextField(max_length=500)),
                ('movie_poster', models.ImageField(blank=True, upload_to='')),
                ('directors', django_mysql.models.ListCharField(models.CharField(max_length=500), blank=True, max_length=3000, size=None)),
                ('trailer_url', models.URLField()),
                ('cast', django_mysql.models.ListCharField(models.CharField(max_length=225), blank=True, max_length=2475, size=None)),
                ('genre', django_mysql.models.ListCharField(models.CharField(max_length=225), blank=True, max_length=2805, size=None)),
                ('avg_rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('country', models.CharField(max_length=100)),
                ('language', models.CharField(max_length=100)),
                ('budget', models.BigIntegerField(blank=True)),
                ('revenue', models.BigIntegerField(blank=True)),
                ('runtime', models.DurationField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField(auto_now_add=True)),
                ('review_text', models.TextField(max_length=2000)),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('movie', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.Movie')),
                ('reviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
