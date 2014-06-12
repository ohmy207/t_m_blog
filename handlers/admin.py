from tornado.web import authenticated, RequestHandler
from bson.objectid import ObjectId
from . import BaseHandler
from config import settings
from procedure import DataProc

class IndexHandler(BaseHandler):
	@authenticated
	def get(self):
		self.redirect("/admin/docs")

class LoginHandler(RequestHandler, DataProc):
	def get(self):
		if self.get_current_user():
			self.redirect("/admin")
			return
		error_msg = self.get_argument("err", None)
		self.render("login.html", error_msg=error_msg)

	def post(self):
		username = self.get_argument("username", None)
		password = self.get_argument("pass", None)
		if username == settings['username'] and password == settings['password']:
			self.set_secure_cookie("user", 'adm')
			self.redirect("/admin")
		else:
			user = self.get_one("user",
					username = username,
					password = password
				)	
			if user:
				self.set_secure_cookie("user", user['username'])
				self.redirect("/admin")
			else:
				self.redirect("/admin/login?err=1")

class LogoutHandler(RequestHandler):
	def get(self):
		self.clear_all_cookies()
		self.redirect("/admin/login")
		
class AuthorHandler(RequestHandler, DataProc):
	def get(self):
		users = self.get_list("user")
		self.render("author_add.html",
				users = users,
				author = "adm"
				)

	def post(self):
		username = self.get_argument("username")
		password = self.get_argument("password")
		self.insert("user", 
				username = username,
				password = password,
				)
		self.redirect("/admin/add_author")

class EditHandler(BaseHandler, DataProc):
	def get(self, user_id):
		user = self.get_one("user", _id=ObjectId(user_id))
		self.render(
			"user_edit.html",
			user = user,
			author = "adm"
		)

	def post(self, user_id):	
		self.update("user", dict(_id = ObjectId(user_id)), password = self.get_argument("password").strip())
		self.redirect("/admin/add_author")

class DeleteHandler(BaseHandler, DataProc):
	def get(self, user_id):
		user = self.get_one("user", _id=ObjectId(user_id))
		self.render(
			"user_del.html",
			user = user,
			author = "adm"
		)	

	def post(self, user_id):
		self.remove_one("user", dict(_id = ObjectId(user_id)))
		self.redirect("/admin/add_author")
