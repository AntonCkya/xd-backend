import sqlite3
from models import SimpleMovie, Movie

class SimpleMovieDB:

	"""
	SimpleMovieBD - класс для работы с базой данных фильмов в простом виде (название, id кинопоиска)
	название типа text, id кинопоиска типа int primary key.
	Методы:	
	__init__ - конструктор объекта, создает бд если не создана
	post - обрабатывает простой Post запрос к серверу: добавляет в бд новый фильм
	get - обрабатывает простой get запрос: получение объекта SimpleMovie из бд по id кинопоиска
	delete - обрабатывает простой delete запрос: удаление объекта SimpleMovie из бд по id кинопоиска
	get_all - получение всех данных из таблицы (если данных много вызовет сущий кошмар)
	"""

	conn = sqlite3.connect('simplemovie.db')
	cur = conn.cursor()

	def __init__(self):
		self.cur.execute("""
					CREATE TABLE IF NOT EXISTS simplemovie
					(
					title TEXT,
					id_kinopoisk INT PRIMARY KEY
					);
					""")
		self.conn.commit()

	def post(self, sm: SimpleMovie):
		self.cur.execute("""
					INSERT INTO simplemovie
   					VALUES(?, ?);
   					""", [sm.title, sm.id_kinopoisk])
		self.conn.commit()

	def get(self, id: int):
		self.cur.execute("""
					SELECT * 
					FROM simplemovie
					WHERE id_kinopoisk = ?;
					""", (id,))
		res = self.cur.fetchone()
		return res

	def delete(self, id: int):
		self.cur.execute("""
					DELETE
					FROM simplemovie
					WHERE id_kinopoisk = ?;
					""", (id,))
		self.conn.commit()

	def update(self, id_prev: int, title_new: str):
		self.cur.execute("""
					UPDATE simplemovie
					SET
					title = ?
					WHERE id_kinopoisk = ?;
					""", [title_new, id_prev])
		self.conn.commit()

	def get_all(self):
		self.cur.execute("""
					SELECT * 
					FROM simplemovie;
					""")
		res = self.cur.fetchall()
		return res


class MovieDB:

	"""
	MovieBD - класс для работы с базой данных фильмов.

	Поля:
	title - название фильма
	description - описание фильма
	id_kinopoisk - id фильма на кинопоиске (primary key)
	cover TEXT - обложка фильма (в виде URL)
	year INT - год выхода
	country TEXT - страна(ы) производства (в виде строки, парсить в случае чего буду не я)
	genres TEXT - жанр(ы) фильма (в виде строки, парсить в случае чего буду не я)
	popularity - популярность (числовое поле, вычисляется по числу кликов на стороне клиента)

	Методы:
	__init__ - конструктор объекта, создает бд если не создана
	post_movie - заливает фильм в бд
	get_movie_by_id - возвращает все данные о фильме по id кинопоиска
	delete_movie_by_id - удаляет фильм из бд по id кинопоиска
	update_movie_by_id - меняет данные о фильме по id кинопоиска (на вход id кинопоиска и объект фильма)
	update_popularity - увеличивает популярность фильма на заданное число по id кинопоиска
	get_movie_popular - возвращает список фильмов заданной длины, отсортированный по популярности
	get_movie_novelty - возвращает список фильмов заданной длины, отсортированный по году выхода
	get_movie_many - возвращает список фильмов заданной длины
	"""

	conn = sqlite3.connect('movie.db')
	cur = conn.cursor()

	def __init__(self):
		self.cur.execute("""
					CREATE TABLE IF NOT EXISTS movie
					(
					title TEXT UNIQUE,
					description TEXT,
					id_kinopoisk INT PRIMARY KEY,
					cover TEXT,
					premiere_date TEXT,
					country TEXT,
					genres TEXT,
					popularity INT,
					age INT,
					producer TEXT,
					webtorrent TEXT
					);
					""")
		self.conn.commit()

	def post_movie(self, movie: Movie):
		self.cur.execute("""
					INSERT INTO movie
   					VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
   					""", [
   						movie.title,
   						movie.description,
   						movie.id_kinopoisk,
   						movie.cover,
   						movie.premiere_date,
   						movie.country,
   						movie.genres,
   						movie.popularity,
   						movie.age,
   						movie.producer,
   						movie.webtorrent
   					])
		self.conn.commit()

	def get_movie_by_id(self, id: int):
		self.cur.execute("""
					SELECT * 
					FROM movie
					WHERE id_kinopoisk = ?;
					""", (id,))
		res = self.cur.fetchone()
		return res

	def delete_movie_by_id(self, id: int):
		self.cur.execute("""
					DELETE
					FROM movie
					WHERE id_kinopoisk = ?;
					""", (id,))
		self.conn.commit()

	def update_movie_by_id(self, id_prev: int, new_movie: Movie):
		self.cur.execute("""
					UPDATE movie
					SET
					title = ?,
					description = ?,
					cover = ?,
					premiere_date = ?,
					country = ?,
					genres = ?,
					popularity = ?,
					age = ?,
					producer = ?
					webtorrent = ?
					WHERE id_kinopoisk = ?;
					""", [
   						new_movie.title,
   						new_movie.description,
   						new_movie.cover,
   						new_movie.premiere_date,
   						new_movie.country,
   						new_movie.genres,
   						new_movie.popularity,
   						new_movie.age,
   						new_movie.producer,
   						new_movie.webtorrent,
   						id_prev
   					])
		self.conn.commit()

	def update_popularity(self, id: int, new_popularity: int):
		self.cur.execute("""
					SELECT popularity 
					FROM movie
					WHERE id_kinopoisk = ?;
					""", (id,))
		res = self.cur.fetchone()
		self.cur.execute("""
					UPDATE movie
					SET
					popularity = ?
					WHERE id_kinopoisk = ?;
					""", [
   						new_popularity + res[0],
   						id
   					])
		self.conn.commit()

	def get_movie_popular (self, count: int):
		self.cur.execute("""
					SELECT * 
					FROM movie
					ORDER BY popularity DESC;
					""")
		res = self.cur.fetchmany(count)
		return res

	def get_movie_novelty (self, count: int):
		self.cur.execute("""
					SELECT * 
					FROM movie
					ORDER BY date(premiere_date) DESC;
					""")
		res = self.cur.fetchmany(count)
		return res

	def get_movie_many (self, count: int):
		self.cur.execute("""
					SELECT * 
					FROM movie;
					""")
		res = self.cur.fetchmany(count)
		return res

	def get_movie_title (self, id: int):
		self.cur.execute("""
					SELECT title 
					FROM movie
					WHERE id_kinopoisk = ?;
					""", (id,))
		res = self.cur.fetchone()
		return res

	def get_movie_webtorrent (self, id: int):
		self.cur.execute("""
					SELECT webtorrent 
					FROM movie
					WHERE id_kinopoisk = ?;
					""", (id,))
		res = self.cur.fetchone()
		return res

	def get_movie_by_title (self, title: str):
		self.cur.execute("""
					SELECT * 
					FROM movie
					WHERE trim(title) LIKE ?;
					""", (title,))
		res = self.cur.fetchone()
		return res
