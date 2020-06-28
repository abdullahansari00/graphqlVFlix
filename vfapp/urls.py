from django.conf.urls import include, url
from . import views
from graphene_django.views import GraphQLView
from .schema import schema
from django.urls import path
#from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
	url(r'^signup/$', views.signup, name = 'signup'),
	url(r'^login/$', views.enter, name = 'enter'),
	url(r'^logout/$', views.exit, name = 'exit'),
	url(r'^$', views.home, name = 'home'),
	url(r'^get_movies/$', views.get_movies, name = 'get_movies'),
	url(r'^graphql/$', GraphQLView.as_view(graphiql=True, schema=schema), name = 'graphql'),
	#path("graphql", GraphQLView.as_view(graphiql=True)),
]

#urlpatterns = format_suffix_patterns(urlpatterns)