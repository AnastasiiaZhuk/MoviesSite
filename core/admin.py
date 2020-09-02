from django.contrib import admin

from core.models import Movie, Role, Person, Vote


admin.site.register(Movie)
admin.site.register(Role)
admin.site.register(Person)
admin.site.register(Vote)
# Register your models here.
