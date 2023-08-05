from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Movie(models.Model):
    title = models.CharField(max_length=200)
    year = models.PositiveIntegerField(validators=[MinValueValidator(1900), MaxValueValidator(2100)])
    rated = models.CharField(max_length=200, default=None, null=True)
    released = models.DateField()
    runtime = models.CharField(max_length=25)
    genre = models.CharField(max_length=200)
    director = models.CharField(max_length=200)
    writer = models.TextField()
    actors = models.TextField()
    plot = models.TextField(default=None, null=True)
    language = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    awards = models.TextField(default=None, null=True)
    poster = models.URLField(max_length=1000, default=None, null=True)
    metascore = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)],
                                            default=None, null=True)
    imdb_rating = models.DecimalField(max_digits=3, decimal_places=1, default=None, null=True)
    imdb_votes = models.PositiveIntegerField(default=None, null=True)
    imdb_id = models.CharField(max_length=25, default=None, null=True)
    type = models.CharField(max_length=50)
    dvd = models.DateField(default=None, null=True)
    box_office = models.IntegerField(default=None, null=True)
    production = models.CharField(max_length=200, default=None, null=True)
    website = models.URLField(max_length=1000, default=None, null=True)

    def __str__(self):
        return self.title


class MovieRatings(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    source = models.CharField(max_length=200)
    value = models.CharField(max_length=25)

    def __str__(self):
        return self.source + ": " + self.value


class Comments(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    comment = models.TextField()

    def __str__(self):
        return self.comment

