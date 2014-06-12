import tornado.web
from config import settings
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

class BaseHandler(tornado.web.RequestHandler):
	def get_current_user(self):
		return self.get_secure_cookie("user")

	def render(self, template_name, **kwargs):
		if not self.request.path.startswith("/admin"):
			template_name = settings["theme"] + '/' + template_name
		super(BaseHandler, self).render(
			template_name,
			settings = settings,
			**kwargs
		)
	def render_string(self, template_name, **kwargs):
		if r.exists(self.request.uri):
			print '===========read from redis cache=========='
			return r.get(self.request.uri)
		print '-------------normal-------------'
		html_generated = super(BaseHandler, self).render_string(
				template_name,
				**kwargs
			)
		if not self.request.path.startswith("/admin"):
			r.set(self.request.uri, html_generated)
		return html_generated

def flush_cache(func):
	def wrapper(*args, **kwargs):
		func(*args, **kwargs)
		r.flushdb()
	return wrapper	
