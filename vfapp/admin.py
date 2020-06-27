from django.contrib import admin
from .models import MoviesInfo, WatchedList
# Register your models here.

admin.site.register(MoviesInfo)
admin.site.register(WatchedList)