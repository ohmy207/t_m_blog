from urls import urls
import tornado.web
import os
import config
import uimodules

settings = config.settings
settings.update(dict(ui_modules=uimodules))

class Application(tornado.web.Application):
	def __init__(self):
		super(Application, self).__init__(
			handlers=urls,
			**settings
			)
