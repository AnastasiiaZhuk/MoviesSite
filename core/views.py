from django.shortcuts import render
from django.views.generic import ListView, DetailView

from core.models import Movie, Person


class MovieListView(ListView):
    model = Movie
    context_object_name = 'movie_list'


class MovieDetailView(DetailView):
    queryset = (Movie.objects.all_with_related_persons())
    context_object_name = 'movie_detail'


class PersonListDetail(ListView):
    queryset = Person.objects.all_with_prefetch_movies()
    context_object_name = 'person'