from datetime import datetime
from decimal import Decimal
from django.core.exceptions import FieldDoesNotExist
from movies_api.models import Movie, MovieRatings
from django.forms.models import model_to_dict
import json


def add_movie(response_data):
    movie = Movie(
        title=response_data['Title'],
        year=response_data['Year'],
        rated=null_if_na(response_data['Rated']),
        released=datetime.strptime(response_data['Released'], "%d %b %Y"),
        runtime=response_data['Runtime'],
        genre=response_data['Genre'],
        director=response_data['Director'],
        writer=response_data['Writer'],
        actors=response_data['Actors'],
        plot=null_if_na(response_data['Plot']),
        language=response_data['Language'],
        country=response_data['Country'],
        awards=null_if_na(response_data['Awards']),
        poster=null_if_na(response_data['Poster']),
        metascore=null_if_na(response_data['Metascore'], 'int'),
        imdb_rating=null_if_na(response_data['imdbRating'], 'decimal'),
        imdb_votes=null_if_na(response_data['imdbVotes'], 'int'),
        imdb_id=null_if_na(response_data['imdbID']),
        type=response_data['Type'],
        dvd=null_if_na(response_data['DVD'], 'date'),
        box_office=null_if_na(response_data['BoxOffice'], 'int'),
        production=null_if_na(response_data['Production']),
        website=null_if_na(response_data['Website'])
    )
    movie.save()

    for rating_data in response_data['Ratings']:
        movie_rating = MovieRatings()
        movie_rating.movie_id = movie.id
        movie_rating.source = rating_data['Source']
        movie_rating.value = rating_data['Value']
        movie_rating.save()

    return Movie.objects.prefetch_related('movieratings_set').get(id=movie.id)


def null_if_na(value, out_type=None):
    if value == "N/A":
        return None

    if out_type:
        if out_type == 'decimal':
            return Decimal(value)

        if out_type == 'date':
            return datetime.strptime(value, "%d %b %Y")

        if out_type == 'int':
            value = value.replace(',', '').replace('$', '')
            return int(value)

    return value


def movie_to_dic(obj):
    movie = model_to_dict(obj)
    movie['ratings'] = list(obj.movieratings_set.values())
    return movie


def response_to_json(response):
    content = response.content.decode("utf-8")
    json_object = json.loads(content)

    return json_object


def get_movies(sort_by, sort_type):
    movie_queryset = Movie.objects.prefetch_related('movieratings_set')

    # TODO: add filtering
    movie_queryset = movie_queryset.all()

    if sort_by:
        try:
            Movie._meta.get_field(str.lower(sort_by))

            if sort_type and str.lower(sort_type) == 'desc':
                movie_queryset = movie_queryset.order_by('-' + sort_by)
            else:
                movie_queryset = movie_queryset.order_by(sort_by)
        except FieldDoesNotExist:
            pass

    return movie_queryset

