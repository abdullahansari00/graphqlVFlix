from django.db import models

# Create your models here.
class MoviesInfo(models.Model):
	popularity = models.FloatField(null=True)
	vote_count = models.IntegerField(null=True)
	poster_path = models.CharField(max_length=100, null=True)
	movie_id = models.IntegerField(null=True)
	adult = models.BooleanField(null=True)
	language = models.TextField(null=True)
	genres = models.CharField(max_length=100, null=True)
	title = models.CharField(max_length=50, null=True)
	vote_average = models.IntegerField(null=True)
	overview = models.CharField(max_length=500, null=True)
	release_date = models.DateField(null=True)

	def __str__(self):
		return(self.title)

class WatchedList(models.Model):
	username = models.CharField(max_length=50)
	movie_ids = models.CharField(max_length=100, default='0')

	def __str__(self):
		return(self.username)