from django.db import models
import json
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import *
from django_mysql.models import ListCharField


# Create your models here.
class Movie(models.Model):
    movie_name = models.CharField(max_length = 100, unique = True)
    release_date = models.DateField()
    description = models.TextField(max_length = 500)
    movie_poster = models.ImageField(blank = True)
    directors = ListCharField(
        base_field = models.CharField(max_length = 500),
        max_length = 6 * 500,
        blank = True
        )
    trailer_url = models.URLField()
    cast = ListCharField(
        base_field = models.CharField(max_length = 225),
        max_length = 11 * 225,
        blank = True
        )
    genre = ListCharField(
        base_field = models.CharField(max_length = 225),
        max_length = 11 * 255,
        blank = True
        )
    avg_rating = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(5)])
    num_ratings = models.IntegerField()
    country = models.CharField(max_length = 100)
    language = models.CharField(max_length = 100)
    budget = models.BigIntegerField()
    revenue = models.BigIntegerField()
    runtime = models.DurationField()



    def __str__(self):
        return self.movie_name



class Review(models.Model):
    reviewer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, )
    created_on = models.DateField(auto_now_add = True)
    review_text = models.TextField(max_length = 2000)
    movie = models.ForeignKey(Movie, on_delete = models.CASCADE)
    rating = models.FloatField(validators = [MinValueValidator(0), MaxValueValidator(5)])

    def save(self, *args, **kwargs):
        if not self.pk:
            rating = Review.objects.filter(movie = self.movie)
            if len(rating) > 0:
                avr_r =  sum([obj.rating for obj in rating]) + self.rating
                num_r = len(rating) + 1
            else:
                avr_r = self.rating
                num_r = 1
            Movie.objects.filter(pk = self.movie.id).update(avg_rating = avr_r/num_r)
            Movie.objects.filter(pk = self.movie.id).update(num_ratings = num_r)
            super().save(*args, **kwargs)
