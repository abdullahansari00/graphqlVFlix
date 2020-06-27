from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
import requests
from .models import MoviesInfo, WatchedList
#tmdb.API_KEY = 'cc4b67c52acb514bdf4931f7cedfd12b'


def home(request):
	if not request.user.is_authenticated:
		return redirect('enter')
	username = request.user.username

	return render(request, 'front/home.html', {'username':username})

def get_movies(request):
	genre_codes = {28:"Action", 12:"Adventure", 16:"Animation", 35:"Comedy", 80:"Crime", 99:"Documentary", 18:"Drama", 10751:"Family", 
				14:"Fantasy", 36:"History", 27:"Horror", 10402:"Music", 9648:"Mystery", 10749:"Romance", 878:"Science Fiction", 
				10770:"TV Movie", 53:"Thriller", 10752:"War", 37:"Western"}

	for y in range(1,501):
		url = 'https://api.themoviedb.org/3/discover/movie?api_key=cc4b67c52acb514bdf4931f7cedfd12b&language=en-US&sort_by=popularity.desc&include_adult=true&include_video=false&page='+str(y)
		response = requests.get(url).json()
		data = response['results']
		for x in data:
			try:
				popularity = x['popularity']
				vote_count = x['vote_count']
				poster_path = x['poster_path']
				movie_id = x['id']
				adult = (x['adult'])
				language = x['original_language']
				genres = x['genre_ids']
				genres = list(map(genre_codes.get, genres))
				genres = ", ".join(map(str, genres))
				title = x['title']
				vote_average = x['vote_average']
				overview = x['overview']
				release_date = x['release_date']

				movie_info = MoviesInfo(popularity=popularity, vote_count=vote_count, poster_path=poster_path, movie_id=movie_id, adult=adult, 
					language=language, genres=genres, title=title, vote_average=vote_average, overview=overview, 
					release_date=release_date)
				#movie_info.save()
			except:
				pass

	return HttpResponse("Success")

def signup(request):
	if request.method == 'POST':
		uname = request.POST.get('uname')
		pword = request.POST.get('pword')
		vpword = request.POST.get('vpword')

		if pword == vpword:
			if len(User.objects.filter(username = uname)) == 0:
				user = User.objects.create_user(username = uname, password = pword)
				w_list = WatchedList(username = uname)
				w_list.save()
				return redirect('home')

			else:
				HttpResponse("Username already exists")
		else:
			HttpResponse("Password not verified")

	return render(request, 'front/signup.html')

def enter(request):
	if request.method == 'POST':
		uname = request.POST.get('uname')
		pword = request.POST.get('pword')

		user = authenticate(username=uname, password=pword)

		if user:
			login(request, user)
			return redirect('home')
		else:
			return HttpResponse("Incorrect username or password")

	return render(request, 'front/login.html')

def exit(request):
	logout(request)
	return redirect('enter')