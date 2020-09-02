from django.views.generic import UpdateView, CreateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

from core.forms import VoteForm, MovieImageForm
from core.models import Movie, Person, Vote, MovieImage


class CreateVote(LoginRequiredMixin, CreateView):
    form_class = VoteForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs.get('movie_id')
        return initial

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse('core:movie_detail', kwargs={'pk': movie_id})

    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs.get('movie_id')
        movie_detail_url = reverse(
            'core:movie_detail',
            kwargs={'pk': movie_id}
        )
        return redirect(to=movie_detail_url)


class UpdateVote(LoginRequiredMixin, UpdateView):
    form_class = VoteForm
    queryset = Vote.objects.all()

    def get_object(self, queryset=None):
        vote = super().get_object(queryset)
        user = self.request.user
        if vote.user != user:
            raise PermissionDenied('cannot change another'
                                   ' users vote')
        return vote

    def get_success_url(self):
        movie_id = self.object.movie.id
        return reverse(
            'core:movie_detail',
            kwargs={'pk': movie_id},
        )

    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs.get('movie_id')
        movie_detail_url = reverse(
            'core:movie_detail',
            kwargs={'pk': movie_id},
        )
        return redirect(to=movie_detail_url)


class MovieListView(ListView):
    model = Movie
    context_object_name = 'movie_list'


class MovieDetailView(DetailView):
    queryset = (Movie.objects.all_with_related_persons_and_score())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image_form'] = self.movie_image_form()

        if self.request.user.is_authenticated:
            vote = Vote.objects.get_vote_or_unsaved_blank_vote(
                movie=self.object,
                user=self.request.user,
            )
            if vote.id:
                vote_form_url = reverse(
                    'core:update_vote',
                    kwargs={
                        'movie_id': vote.movie.id,
                        'pk': vote.id,
                    }
                )
            else:
                vote_form_url = (
                    reverse(
                        'core:create_vote',
                        kwargs={
                            'movie_id': self.object.id
                        }
                    )
                )
            vote_form = VoteForm(instance=vote)
            context['vote_form'] = vote_form
            context['vote_form_url'] = vote_form_url
        return context

    def movie_image_form(self):
        if self.request.user.is_authenticated:
            return MovieImageForm()
        return None

    context_object_name = 'movie_detail'


class PersonListDetail(ListView):
    queryset = Person.objects.all_with_prefetch_movies()
    context_object_name = 'person'


class MovieImageUpload(LoginRequiredMixin, CreateView):
    form_class = MovieImageForm

    def get_initial(self):
        initial = super().get_initial()
        initial['user'] = self.request.user.id
        initial['movie'] = self.kwargs.get('movie_id')
        return initial

    def render_to_response(self, context, **response_kwargs):
        movie_id = self.kwargs.get('movie_id')
        movie_detail_url = reverse('core:movie_detail', kwargs={'pk': movie_id})
        return redirect(to=movie_detail_url)

    def get_success_url(self):
        movie_id = self.kwargs.get('movie_id')
        movie_detail_url = reverse('core:movie_detail', kwargs={'pk': movie_id})
        return movie_detail_url

