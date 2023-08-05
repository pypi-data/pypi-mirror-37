from django import forms

from movies_api.models import Movie


class MoviesPostForm(forms.Form):
    title = forms.CharField(max_length=200)


class CommentsPostForm(forms.Form):
    movie_id = forms.ModelChoiceField(queryset=Movie.objects.all())
    comment = forms.CharField()
