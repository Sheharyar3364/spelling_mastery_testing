from django.contrib import admin

from .models import Answer, Puzzle, UserGame

# Register your models here.
admin.site.register(Puzzle)
admin.site.register(Answer)
admin.site.register(UserGame)