from django.contrib import admin
from .models import Movie, MovieRatings, Comments

admin.site.register(Movie)
admin.site.register(MovieRatings)
admin.site.register(Comments)
