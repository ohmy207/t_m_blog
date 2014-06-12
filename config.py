import os.path

settings = dict(
		blog_name = u"T_M_Blog",
		username = "admin",
		password="111111",
		email="share@email"
		template_path = os.path.join(os.path.dirname(__file__), "templates"),
		static_path = os.path.join(os.path.dirname(__file__), "static"),
		login_url = "/admin/login",
		cookie_secret = "cookie_secret",
		theme="modernist",
		debug = True,
		navigate = [
			dict(name="Home", link="/")
			],
		index_page_size = 5,
		admin_page_size = 20
		)

DB_PORT = 27017
DB_HOST = "localhost"
BLOG_DB = "t_m_blog"
PORT = 8888

Redis_HOST = "localhost"
Redis_PORT = 6379
Redis_DB = 0
