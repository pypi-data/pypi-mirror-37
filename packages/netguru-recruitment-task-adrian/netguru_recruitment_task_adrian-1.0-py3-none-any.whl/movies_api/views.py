from datetime import datetime
from django.db.models import Count
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from movies_api.models import Movie, Comments
from movies_api.modules.omdbapi import OmdbAPI
from movies_api.utils import add_movie, movie_to_dic, get_movies
from movies_api.forms import MoviesPostForm, CommentsPostForm
import json
from django.forms.models import model_to_dict
from django.core.serializers.json import DjangoJSONEncoder


@csrf_exempt
def movies(request, movie_id=None):
    if request.method == 'POST':
        return movies_post(request.POST)

    return movies_get(request.GET, movie_id)


def movies_post(POST):
    form = MoviesPostForm(POST)
    if form.is_valid():
        title = form.cleaned_data['title']

        # check if already added to db
        movie_exist = Movie.objects.filter(title__iexact=title).first()
        if movie_exist:
            serialized = json.dumps(movie_to_dic(movie_exist), cls=DjangoJSONEncoder)
            return HttpResponse(serialized, content_type='application/json')

        # get details
        response = OmdbAPI().get_movie_details(title)
        response_data = json.loads(response.decode('utf-8'))

        # check if found in OMDB database
        if response_data['Response'] == 'False':
            return JsonResponse({'error': 'Movie not found in OMDB'}, status=404)

        # add movie
        obj = add_movie(response_data)

        serialized = json.dumps(movie_to_dic(obj), cls=DjangoJSONEncoder)
        return HttpResponse(serialized, content_type='application/json')

    return JsonResponse({'error': form.errors}, status=400)


def movies_get(GET, movie_id):
    if movie_id:
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return JsonResponse({'error': 'Movie not found'}, status=404)

        movies_ = movie_to_dic(movie)

    else:
        sort_by = GET.get('sort_by', None)
        sort_type = GET.get('sort_type', None)

        movie_queryset = get_movies(sort_by, sort_type)

        movies_ = []
        for obj in movie_queryset:
            movies_.append(movie_to_dic(obj))

    serialized = json.dumps(movies_, cls=DjangoJSONEncoder)
    return HttpResponse(serialized, content_type='application/json')


@csrf_exempt
def comments(request, comment_id=None):
    if request.method == 'POST' and not comment_id:
        return comments_post(request.POST)

    return comments_get(comment_id)


def comments_post(POST):
    form = CommentsPostForm(POST)
    if form.is_valid():
        movie_id = form.cleaned_data['movie_id']
        comment_text = form.cleaned_data['comment']

        comment = Comments()
        comment.movie_id = movie_id.id
        comment.comment = comment_text
        comment.save()

        dic = model_to_dict(comment)

        serialized = json.dumps(dic, cls=DjangoJSONEncoder)
        return HttpResponse(serialized, content_type='application/json')

    return JsonResponse({'error': form.errors}, status=400)


def comments_get(comment_id):
    if comment_id:
        try:
            comment = Comments.objects.get(id=comment_id)
        except Comments.DoesNotExist:
            return JsonResponse({'error': 'Comment not found'}, status=404)

        comments_ = model_to_dict(comment)

    else:
        comments_queryset = Comments.objects.all()

        comments_ = []
        for obj in comments_queryset:
            comments_.append(model_to_dict(obj))

    serialized = json.dumps(comments_, cls=DjangoJSONEncoder)
    return HttpResponse(serialized, content_type='application/json')


def top(request, from_date, to_date):
    try:
        from_date = datetime.strptime(from_date, "%Y-%m-%d").date()
        to_date = datetime.strptime(to_date, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({'error': 'Wrong dates format'}, status=400)

    comments_queryset = Comments.objects.values('movie_id')\
        .annotate(total_comments=Count('movie_id'))\
        .filter(movie__released__range=(from_date, to_date))\
        .order_by('-total_comments')

    comments_toplist = []

    rank = 1
    last_total_comments = None
    for comment in comments_queryset:
        if not last_total_comments:
            last_total_comments = comment['total_comments']

        if comment['total_comments'] < last_total_comments:
            last_total_comments = comment['total_comments']
            rank += 1

        comments_toplist.append(
            {'movie_id': comment['movie_id'], 'total_comments': comment['total_comments'], 'rank': rank}
        )

    return JsonResponse(comments_toplist, safe=False)
