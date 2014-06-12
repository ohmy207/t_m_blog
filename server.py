import tornado.ioloop
import sys
import config
from application import Application

def main():
	application = Application()
	application.listen(config.PORT)
	tornado.ioloop.IOLoop.instance().start()

if __name__ == "__main__":
	main()
