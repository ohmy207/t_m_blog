from . import BaseHandler, flush_cache
from procedure import DataProc
from config import settings
from bson.objectid import ObjectId
from datetime import datetime

class IndexHandler(BaseHandler, DataProc):
	def get(self):
		tag = self.get_argument("tag", None)
		current_page = int(self.get_argument("p", 1))
		total = self.count("doc")
		docs = self.get_by_page(current_page, settings['index_page_size'], "doc")
		print self.render(
			"index.html",
			tag = tag,
			articles = docs,
			total = total,
			current_page = current_page,
		)

class ArticleHandler(BaseHandler, DataProc):		
	def get(self, doc_id):
		doc = self.get_one("doc", _id = ObjectId(doc_id))
		tags = doc['tags']
		select_tags = []
		for i in range(len(tags)):
			tags[i] = ObjectId(tags[i])
		for item in	tags:
			select_tags.append(self.get_one("tags", _id = item))
		comments = doc['comments']	
		self.render(
			"article.html",
			article = doc,
			tags = select_tags,
			comments = comments
		)	
	
	@flush_cache	
	def post(self, doc_id):	
		comments = self.get_one("doc", _id = ObjectId(doc_id))['comments']
		comment = dict(
				nickname = self.get_argument("nickname"),
				email = self.get_argument("email"),
				content = self.get_argument("content"),
				post_time = datetime.now()
				)
		comments.append(comment)
		self.update(
			"doc",
			dict(_id = ObjectId(doc_id)),
			comments = comments
		)	
		self.redirect("/article/" + doc_id)	
