from django.urls import path

from core.views import MovieListView, MovieDetailView


app_name = 'core'

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail')
]