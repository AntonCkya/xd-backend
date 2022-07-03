import hashlib

class PasswordHash:

	"""
	PasswordHash - класс с методами для хэширования паролей
	hash_password - хэширует пароль (sha256)
	hash_compare - сопоставляет пароль с хэшем
	"""

	def hash_password(self, password: str):
		hash_object = hashlib.sha256(bytes(password, 'utf-8'))
		return hash_object.hexdigest()


	def hash_compare(self, password: str, hash: str):
		hash_object = hashlib.sha256(bytes(password, 'utf-8'))
		return hash_object.hexdigest() == hash


class PasswordSafety:

	"""
	PasswordSafety - класс с методами на проверку безопасности пароля
	number_in_password - проверка на наличие цифры в пароле
	liter_in_password - проверка на наличие латинской буквы в алфавите (в любом регистре)
	lenght_password - проверка на длину пароля (6 и более символов)
	"""

	numlist = list('0123456789')
	literlist = list('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM')

	def number_in_password(self, password: str):
		for i in list(password):
			if i in self.numlist:
				return True
		return False


	def liter_in_password(self, password: str):
		for i in list(password):
			if i in self.literlist:
				return True
		return False


	def lenght_password(self, password: str):
		return len(password) >= 6