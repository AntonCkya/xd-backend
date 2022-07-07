from pydantic import BaseModel, HttpUrl, ValidationError, validator
from typing import List
from datetime import date
from password import PasswordSafety

class Movie (BaseModel):
	title : str
	description : str
	id_kinopoisk : int
	cover : HttpUrl = None
	premiere_date : date
	country : str
	genres : str
	popularity : int
	age: int
	producer: str
	webtorrent: str

class SimpleMovie (BaseModel):
	title : str
	id_kinopoisk : int

class User (BaseModel):
	name: str
	password: str
	password_verify: str

	@validator('password_verify')
	def passwords_match(cls, password_verify, values, **kwargs):
		if 'password' in values and password_verify != values['password']:
			raise ValueError('passwords do not match')
		return password_verify

	@validator('password')
	def password_safety(cls, password):
		passsafe = PasswordSafety()
		if not passsafe.number_in_password(password):
			raise ValueError('passwords does not contain a number')
		if not passsafe.liter_in_password(password):
			raise ValueError('passwords does not contain a latin letter')
		if not passsafe.lenght_password(password):
			raise ValueError('password length less than 6')
		return password
