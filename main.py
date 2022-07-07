from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

from models import Movie
from database import MovieDB

app = FastAPI()
mdb = MovieDB()

@app.get('/')
async def test():
	return {"message": "success"}

@app.post('/post_movie/')
async def post_movie(mv: Movie):
	mdb.post_movie(mv)
	return {"message": "success"}

@app.get('/get_movie/')
async def get_movie(id: int):
	res = mdb.get_movie_by_id(id)
	return {
		'title': res[0],
		'description': res[1],
		'id_kinopoisk': res[2],
		'cover': res[3],
		'premiere_date': res[4],
		'country': res[5],
		'genres': res[6],
		'popularity': res[7],
		'age': res[8],
		'producer': res[9],
		'webtorrent': res[10]
	}

@app.delete('/delete_movie/')
async def delete_movie(id: int):
	mdb.delete_movie_by_id(id)
	return {"message": "success"}

@app.get('/get_movie_popular/')
async def get_movie_popular(count: int):
	many = mdb.get_movie_popular(count)
	l = []
	for res in many:
		l.append(
			{
			'title': res[0],
			'description': res[1],
			'id_kinopoisk': res[2],
			'cover': res[3],
			'premiere_date': res[4],
			'country': res[5],
			'genres': res[6],
			'popularity': res[7],
			'age': res[8],
			'producer': res[9],
			'webtorrent': res[10]
			}
		)
	return {"list": l}

@app.get('/get_movie_novelty/')
async def get_movie_novelty(count: int):
	many = mdb.get_movie_novelty(count)
	l = []
	for res in many:
		l.append(
			{
			'title': res[0],
			'description': res[1],
			'id_kinopoisk': res[2],
			'cover': res[3],
			'premiere_date': res[4],
			'country': res[5],
			'genres': res[6],
			'popularity': res[7],
			'age': res[8],
			'producer': res[9],
			'webtorrent': res[10]
			}
		)
	return {"list": l}

@app.get('/get_movie_many/')
async def get_movie_many(count: int):
	many = mdb.get_movie_many(count)
	l = []
	for res in many:
		l.append(
			{
			'title': res[0],
			'description': res[1],
			'id_kinopoisk': res[2],
			'cover': res[3],
			'premiere_date': res[4],
			'country': res[5],
			'genres': res[6],
			'popularity': res[7],
			'age': res[8],
			'producer': res[9],
			'webtorrent': res[10]
			}
		)
	return {"list": l}

@app.put('/update_popularity/')
async def update_popularity(id: int, pop: int):
	mdb.update_popularity(id, pop)
	return {"message": "success"}

@app.get('/get_movie_title/')
async def get_movie_title(id: int):
	res = mdb.get_movie_title(id)
	return {"title": res[0]}

@app.get('/get_movie_webtorrent/')
async def get_movie_webtorrent(id: int):
	res = mdb.get_movie_webtorrent(id)
	return {"webtorrent": res[0]}

@app.get('/get_movie_by_title/')
async def get_movie_by_title(title: str):
	res = mdb.get_movie_by_title(title)
	print(res)
	return {
		'title': res[0],
		'description': res[1],
		'id_kinopoisk': res[2],
		'cover': res[3],
		'premiere_date': res[4],
		'country': res[5],
		'genres': res[6],
		'popularity': res[7],
		'age': res[8],
		'producer': res[9],
		'webtorrent': res[10]
	}


def custom_openapi():
	if app.openapi_schema:
		return app.openapi_schema
	openapi_schema = get_openapi(
    	title="[ xd ]",
		version="0.0.2",
		description="Первая версия api к онлайн-кинотеатру [ xd ]",
		routes=app.routes,
	)
	app.openapi_schema = openapi_schema
	return app.openapi_schema

app.openapi = custom_openapi
