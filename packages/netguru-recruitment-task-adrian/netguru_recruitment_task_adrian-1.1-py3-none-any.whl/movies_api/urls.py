from django.conf.urls import url
from django.urls import path
from movies_api import views as movies_api_views

urlpatterns = [
    path('movies', movies_api_views.movies, name='movies'),
    path('movies/<int:movie_id>', movies_api_views.movies, name='movies_id'),
    path('comments', movies_api_views.comments, name='comments'),
    path('comments/<int:comment_id>', movies_api_views.comments, name='comments_id'),
    url(r'^top/(?P<from_date>\d{4}-\d{2}-\d{2})/(?P<to_date>\d{4}-\d{2}-\d{2})$', movies_api_views.top, name='top'),
]

