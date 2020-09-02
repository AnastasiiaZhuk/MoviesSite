from django.urls import path

from core.views import CreateVote, UpdateVote, MovieListView, MovieDetailView, MovieImageUpload


app_name = 'core'

urlpatterns = [
    path('movies/', MovieListView.as_view(), name='movie_list'),
    path('movies/<int:pk>/', MovieDetailView.as_view(), name='movie_detail'),
    path('movies/<int:movie_id>/vote/', CreateVote.as_view(), name='create_vote'),
    path('movies/<int:movie_id>/vote/<int:pk>/', UpdateVote.as_view(), name='update_vote'),
    path('movies/<int:movie_id>/image/upload/', MovieImageUpload.as_view(), name='movie_image_upload'),

]