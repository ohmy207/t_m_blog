import tornado.web
from datetime import datetime
from tornado.web import authenticated
from bson.objectid import ObjectId

from config import settings
from procedure import DataProc
from . import BaseHandler, flush_cache

class AddHandler(BaseHandler, DataProc):
	@authenticated
	def get(self):
		self.render(
			"doc_add.html",
			tags=self.get_list("tags"),
			author = self.get_current_user()
		)
	
	@authenticated
	@flush_cache
	def post(self):
		self.insert(
			"doc",
			title = self.get_argument("title"),
			content = self.get_argument("content"),
			tags = self.get_arguments("tags"),
			post_time = datetime.now(),
			comments = [],
			author = self.get_current_user()
		)
		self.redirect("/admin/docs")

class ListHandler(BaseHandler, DataProc):
	@authenticated
	def get(self):
		current_page = int(self.get_argument("p", 1))
		total = self.count("doc")
		author = self.get_current_user()
		if author == "adm":
			docs = self.get_by_page(current_page, settings['index_page_size'], "doc")
		else:
			docs = self.get_by_page(current_page, settings['index_page_size'], "doc", author = author)
		self.render(
			"doc_list.html",
			docs = docs,
			total = total,
			current_page = current_page,
			author = author
			)

class EditHandler(BaseHandler, DataProc):	
	@authenticated
	def get(self, doc_id):
		doc = self.get_one("doc", _id = ObjectId(doc_id))
		selected_tags = doc['tags']
		self.render(
			"doc_edit.html",
			doc =doc,
			tags = self.get_list("tags"),
			selected_tags = selected_tags,
			author = self.get_current_user()
			)
	
	@authenticated
	@flush_cache
	def post(self, doc_id):
		self.update(
			"doc",
			dict(_id = ObjectId(doc_id)),
			title = self.get_argument("title"),
			content = self.get_argument("content"),
			tags = self.get_arguments("tags")
			)
		self.redirect("/admin/docs")

class DeleteHandler(BaseHandler, DataProc):
	@authenticated
	def get(self, doc_id):
		self.render(
			"doc_delete.html",
			doc = self.get_one("doc", _id = ObjectId(doc_id)),
			author = self.get_current_user()
			)

	@authenticated
	@flush_cache
	def post(self, doc_id):
		self.remove_one("doc", dict(_id = ObjectId(doc_id)))
		self.redirect("/admin/docs")

class CommentHandler(BaseHandler, DataProc):
	@authenticated
	def get(self, doc_id):
		doc = self.get_one("doc", _id = ObjectId(doc_id))
		doc_id = doc_id
		comments = doc['comments']
		self.render(
			"doc_comments.html",
			comments = comments,
			doc_id = doc_id,
			author = self.get_current_user()
		)

	@authenticated
	@flush_cache
	def post(self, doc_id):
		comments = self.get_one("doc", _id = ObjectId(doc_id))['comments']
		comment = dict(
				nickname = self.get_current_user(),
				email = settings["email"],
				content = self.get_argument("content"),
				post_time = datetime.now()
				)
		comments.append(comment)
		self.update(
			"doc",
			dict(_id = ObjectId(doc_id)),
			comments = comments
		)	
		self.redirect("/admin/doc/comment/" + doc_id)

class DeleteCommentHandler(BaseHandler, DataProc):		
	@authenticated
	def get(self, comment_id, doc_id):
		comments = self.get_one("doc", _id = ObjectId(doc_id))['comments']
		self.render(
			"comment_delete.html",
			comment = comments[int(comment_id)],
			author = self.get_current_user()
			)

	@authenticated
	@flush_cache
	def post(self, comment_id, doc_id):
		comments = self.get_one("doc", _id = ObjectId(doc_id))['comments']
		del comments[int(comment_id)]
		self.update(
			"doc",
			dict(_id = ObjectId(doc_id)),
			comments = comments
		)
		self.redirect("/admin/doc/comment/" + doc_id)
