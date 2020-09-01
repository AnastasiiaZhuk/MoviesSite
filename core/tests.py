from django.test import TestCase
from django.test.client import RequestFactory
from django.urls.base import reverse

from core.models import Movie
from core.views import MovieListView


class MovieListPaginationTestCase(TestCase):
    ACTIVE_PAGINATION_HTML = """
    <li class="page-item active">
      <a href="{}?page={}" class="page-link">{}</a>
    </li>
    """

    def setUp(self):
        for n in range(15):
            Movie.objects.create(
                title=f'Title {n}',
                year=1990 + n,
                runtime=100,
            )

    def test_first_page(self):
        movie_list_path = reverse(
            'core:movie_list')
        request = RequestFactory().get(
            path=movie_list_path)
        response = MovieListView.as_view()(
            request)
        self.assertEqual(
            200,
            response.status_code)
        self.assertTemplateUsed('core/movie_list.html')
        self.assertTrue(
            response.context_data[
                'is_paginated'])
        self.assertInHTML(
            self.ACTIVE_PAGINATION_HTML.format(
                movie_list_path, 1, 1),
            response.rendered_content)