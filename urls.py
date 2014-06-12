from handlers import index
from handlers import admin
from handlers import tag
from handlers import doc

#handlers url mapping
urls = [
	(r"/admin", admin.IndexHandler),
	(r"/admin/login", admin.LoginHandler),
	(r"/admin/logout", admin.LogoutHandler),
	(r"/admin/add_author", admin.AuthorHandler),
	(r"/admin/author/edit/([a-zA-Z0-9-]+)", admin.EditHandler),
	(r"/admin/author/rm/([a-zA-Z0-9-]+)", admin.DeleteHandler),
	(r"/admin/tags", tag.IndexHandler),
	(r"/admin/tag/edit/([a-zA-Z0-9-]+)", tag.EditHandler),
	(r"/admin/tag/rm/([a-zA-Z0-9-]+)", tag.RemoveHandler),
	(r"/admin/add_doc", doc.AddHandler),
	(r"/admin/docs", doc.ListHandler),
	(r"/admin/doc/edit/([a-zA-Z0-9-]+)", doc.EditHandler),
	(r"/admin/doc/delete/([a-zA-Z0-9-]+)", doc.DeleteHandler),
	(r"/admin/doc/comment/([a-zA-Z0-9-]+)", doc.CommentHandler),
	(r"/admin/doc/delcomment/([a-zA-Z0-9-]+)/([a-zA-Z0-9-]+)", doc.DeleteCommentHandler),
	(r"/", index.IndexHandler),	
	(r"/article/([a-zA-Z0-9-]+)", index.ArticleHandler)
	]
