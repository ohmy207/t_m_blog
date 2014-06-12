import tornado.web
from config import settings

class BaseModule(tornado.web.UIModule):
	def render_string(self, template_name, **kwargs):
		template_name = settings["theme"] + '/' + template_name
		return super(BaseModule, self).render_string(template_name, **kwargs)

class Page(BaseModule):		
	def render(self, total, current_page, is_archive=False):
		prev = current_page - 1
		if is_archive:
			page_size = settings["archive_page_size"]
		else:
			page_size = settings["index_page_size"]
		next = current_page + 1 if page_size * current_page < total else False
		return self.render_string("module/page.html", prev=prev, next=next)

class RecentPosts(BaseModule):
	def render(self, recent_posts):
		return self.render_string("module/recent_posts.html", recent_posts=recent_posts)
