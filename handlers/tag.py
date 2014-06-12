from tornado.web import authenticated
from bson.objectid import ObjectId
from . import BaseHandler, flush_cache
from procedure import DataProc

class IndexHandler(BaseHandler, DataProc):
	@authenticated
	def get(self):
		self.render("tag.html", tags = self.get_list("tags"), author = self.get_current_user())

	@authenticated
	@flush_cache
	def post(self):
		tag_name = self.get_argument("name")
		self.insert("tags", tag = tag_name)
		self.redirect("/admin/tags")

class EditHandler(BaseHandler, DataProc):
	@authenticated
	def get(self, tag_id):
		tag = self.get_one("tags", _id=ObjectId(tag_id))
		self.render(
			"tag_edit.html",
			tag = tag,
			author = self.get_current_user()
		)

	@authenticated
	@flush_cache
	def post(self, tag_id):
		self.update("tags", dict(_id = ObjectId(tag_id)), tag = self.get_argument("tag").strip())
		self.redirect("/admin/tags")

class RemoveHandler(BaseHandler, DataProc):
	@authenticated
	def get(self, tag_id):
		tag = self.get_one("tags", _id=ObjectId(tag_id))
		self.render(
			"tag_delete.html",
			tag = tag,
			author = self.get_current_user()
		)	
	@authenticated
	@flush_cache
	def post(self, tag_id):
		self.remove_one("tags", dict(_id = ObjectId(tag_id)))
		self.redirect("/admin/tags")
