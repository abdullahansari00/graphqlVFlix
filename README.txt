Installations required:
	Python 3
	Django 3.0.7
	Graphene-django 2.11.0

Summary:
	Database has been populated using TMDB API. It solves various queries and allows us to add or delete movies from watched list using mutations as listed below. You will need to login to access these activities. There is already one user created: username: admin, password: root. Visit to address "http://127.0.0.1:8000/" to initiate. Your empty watched list is automatically created when you signup. For clear understanding please refer to screenshots in "Screenshots" folder.

Queries:
	Show all movies
	Search movie by:
		string
		movie id
	Sort movies by:
		latest
		popularity
		upcoming
	Show watched movies list
	Show recommended movies

Mutations:
	Add movie to watched list using movie id
	Delete movie from watched list using movie id