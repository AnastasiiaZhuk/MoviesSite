from django.shortcuts import render
from django.views.generic import ListView, DetailView

from core.models import Movie


class MovieListView(ListView):
    model = Movie
    context_object_name = 'movie_list'


class MovieDetailView(DetailView):
    model = Movie
    context_object_name = 'movie_detail'
