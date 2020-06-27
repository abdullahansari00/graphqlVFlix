import graphene
from graphene_django.types import DjangoObjectType
from graphene_django import DjangoListField
from graphene import relay
from .models import MoviesInfo, WatchedList
from django.utils import timezone
import requests


#Object Types

class MoviesInfoType(DjangoObjectType):
	class Meta:
		model = MoviesInfo
		interfaces = (relay.Node,)
		#fields = ("title",)
	name = graphene.String()

class MoviesInfoConnection(relay.Connection):
	class Meta:
		node = MoviesInfoType

class WatchedListType(DjangoObjectType):
	class Meta:
		model = WatchedList


#Mutations

class AddMovieMutation(graphene.Mutation):
	class Arguments:
		movie_id = graphene.Int()
	watched_list = graphene.Field(WatchedListType)

	def mutate(self, info, movie_id):
		username = info.context.user.username
		watched_list = WatchedList.objects.get(username=username)
		ids = watched_list.movie_ids
		ids = list(map(int, ids.split(",")))
		if movie_id not in ids:
			ids.append(movie_id)
			ids = ", ".join(map(str, ids))
			watched_list.movie_ids = ids
			watched_list.save()
		return(AddMovieMutation(watched_list=watched_list))

class DelMovieMutation(graphene.Mutation):
	class Arguments:
		movie_id = graphene.Int()
	watched_list = graphene.Field(WatchedListType)

	def mutate(self, info, movie_id):
		username = info.context.user.username
		watched_list = WatchedList.objects.get(username=username)
		ids = watched_list.movie_ids
		ids = list(map(int, ids.split(",")))
		ids.remove(movie_id)
		ids = ", ".join(map(str, ids))
		watched_list.movie_ids = ids
		watched_list.save()
		return(DelMovieMutation(watched_list=watched_list))


class Mutation(graphene.ObjectType):
	add_to_watched_list = AddMovieMutation.Field()
	del_from_watched_list = DelMovieMutation.Field()


#Queries

class Query(graphene.ObjectType):
	#all_movies = graphene.List(MoviesInfoType)
	all_movies = relay.ConnectionField(MoviesInfoConnection)
	search = graphene.List(MoviesInfoType, search_by_name=graphene.String(), search_by_id=graphene.Int())
	sort_movies = graphene.List(MoviesInfoType, sort_by=graphene.String())
	watched_movies = graphene.List(MoviesInfoType)
	recommended_movies = graphene.List(MoviesInfoType)


	def resolve_recommended_movies(self, info, **kwargs):
		username = info.context.user.username
		watched_list = WatchedList.objects.get(username=username)
		ids = watched_list.movie_ids
		ids = list(map(int, ids.split(",")))
		try:
			ids.remove(0)
		except:
			pass
		ids = ",".join(map(str, ids))
		recommended_ids = []
		for x in range(1,3):
			url = 'https://api.themoviedb.org/3/movie/'+ids+'/recommendations?api_key=cc4b67c52acb514bdf4931f7cedfd12b&language=en-US&page='+str(x)
			response = requests.get(url).json()['results']
			for x in response:
				recommended_ids.append(x['id'])

		return(MoviesInfo.objects.filter(movie_id__in=recommended_ids))

	def resolve_all_movies(self, info, **kwargs):
		return(MoviesInfo.objects.all())

	def resolve_search(self, info, **kwargs):
		search_by_name = kwargs.get('search_by_name')
		search_by_id = kwargs.get('search_by_id')
		if search_by_name is not None:
			return(MoviesInfo.objects.filter(title__contains=search_by_name))
		elif search_by_id is not None:
			return(MoviesInfo.objects.filter(movie_id=search_by_id))

		return(MoviesInfo.objects.all())

	def resolve_sort_movies(self, info, **kwargs):
		sort_by = kwargs.get('sort_by')

		if sort_by == 'latest':
			return(MoviesInfo.objects.order_by('-release_date'))

		elif sort_by == 'popularity':
			return(MoviesInfo.objects.order_by('-popularity'))

		elif sort_by == 'upcoming':
			now = timezone.now()
			return(MoviesInfo.objects.filter(release_date__gte=now).order_by('release_date'))

		return(MoviesInfo.objects.all())

	def resolve_watched_movies(self, info, **kwargs):
		username = info.context.user.username
		watched_list = WatchedList.objects.get(username=username)
		ids = watched_list.movie_ids
		ids = list(map(int, ids.split(",")))

		return(MoviesInfo.objects.filter(movie_id__in=ids))


schema = graphene.Schema(query=Query, mutation=Mutation)