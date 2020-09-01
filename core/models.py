from django.db import models


class MovieManager(models.Manager):
    def all_with_related_persons(self):
        queryset = self.get_queryset()
        queryset = queryset.select_related('director')
        queryset = queryset.prefetch_related('writers', 'actors')
        return queryset


class Movie(models.Model):

    objects = MovieManager()

    class Meta:
        ordering = ('-year', 'title')
        app_label = 'core'

    NOT_RATED = 0
    RATED_G = 1
    RATED_PG = 2
    RATED_R = 3

    RATINGS = (
        (NOT_RATED, 'NR - Not rated'),
        (RATED_G, 'G - General Audiences '),
        (RATED_PG, 'PG - Parental Guidance ' 'Suggested'),
        (RATED_R, 'R - Restricted'),
    )
    director = models.ForeignKey(
        to='Person',
        on_delete=models.SET_NULL,
        related_name='directed',
        null=True,
        blank=True,
    )
    writers = models.ManyToManyField(
        to='Person',
        related_name='writing_credits',
        blank=True,
    )
    actors = models.ManyToManyField(
        to='Person',
        through='Role',
        related_name='acting_credits',
        blank=True,
    )
    title = models.CharField(max_length=140)
    plot = models.TextField()
    year = models.PositiveIntegerField()
    rating = models.IntegerField(
        choices=RATINGS,
        default=NOT_RATED
    )
    runtime = models.PositiveIntegerField()
    website = models.URLField(blank=True)

    def __str__(self):
        return f'{self.title} {self.year}'


class PersonManager(models.Manager):

    def all_with_prefetch_movies(self):
        queryset = self.get_queryset()
        return queryset.prefetch_related(
            'directed',
            'writing_credits',
            'role_set__movie'
        )


class Person(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    born = models.DateField()
    died = models.DateField(
        null=True,
        blank=True)
    objects = PersonManager()

    class Meta:
        ordering = (
            'last_name', 'first_name')

    def __str__(self):
        if self.died:
            return '{}, {} ({}-{})'.format(
                self.last_name,
                self.first_name,
                self.born,
                self.died)
        return '{}, {} ({})'.format(
            self.last_name,
            self.first_name,
            self.born)


class Role(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.DO_NOTHING)
    person = models.ForeignKey(Person, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=140)

    def __str__(self):
        return f'{self.movie_id} {self.person_id} {self.name}'

    class Meta:
        unique_together = ('movie',
                           'person',
                           'name')