import pymongo
import config

class DataBase:
	def connect(self, db_host, db_port, blog_db):
		conn=pymongo.Connection(db_host,db_port)
		return conn[blog_db]

con = DataBase()
db = con.connect(config.DB_HOST, config.DB_PORT, config.BLOG_DB)
