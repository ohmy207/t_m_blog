from database import db
from  pymongo import DESCENDING


class DataProc:

	def get_one(self, table, **kwargs):
		try:
			find = db[table].find_one(kwargs)
			return find
		except:
			print "404"

	def get_list(self, table, **kwargs):
		try:
			find = db[table].find(kwargs)
			return find
		except:
			print "404"

	def count(self, table, **kwargs):
		find = db[table].count()
		return find

	def insert(self, table, **kwargs):
		rs = db[table].insert(kwargs)
		return rs

	def update(self, table, criteria, **kwargs):
		rs = db[table].update(criteria, {"$set":kwargs})
		return rs

	def remove_one(self, table, criteria):
		rs = db[table].remove(criteria)
		return rs

	def get_start(self, page, page_size):
		start = (page - 1) * page_size
		return start

	def get_by_page(self, page, page_size, table, **kwargs):
		start = self.get_start(page, page_size)
		find = db[table].find(kwargs).sort("post_time",DESCENDING).skip(start).limit(page_size)
		return find		

if __name__ == "__main__":
	bp = DataProc()
	print bp.insert('aa',asd = 123)
	for item in bp.get_list('aa'):print item
