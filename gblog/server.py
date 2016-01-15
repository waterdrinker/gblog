import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape
import signal
import sys
import logging

from gblog import mytorndb
from gblog import config
from gblog import uimodule
from gblog.handlers.multi import *
from gblog.handlers.compose import ComposeHandler
from gblog.handlers.comment import CommentHandler
from gblog.handlers.auth import *
from gblog.handlers.feed import FeedHandler
from gblog.handlers.super import SuperHandler, ProxySuperHandler


class Application(tornado.web.Application):
    def __init__(self):
        urls = [
            (r"/", HomeHandler),
            (r"/about", AboutHandler),
            (r"/archive", ArchiveHandler),
            (r"/feed", FeedHandler),
            (r"/entry/([^/]+)", EntryHandler),
            (r"/comment", CommentHandler),
            (r"/compose", ComposeHandler),
            (r"/auth/login", AuthLoginHandler),
            (r"/auth/google_login", GoogleOAuth2LoginHandler),
            (r"/auth/logout", AuthLogoutHandler),
            (r"/category", CategoryHandler),
            (r"/proxy/supervisor(.*)", ProxySuperHandler),
            (r"/supervisor", SuperHandler),
        ]

        settings = dict(
            blog_title="example's Blog",
            blog_url="example.com",
            config_dir=os.path.expanduser('~') + '/.gblog',
            config_file=os.path.expanduser('~') + '/.gblog/config',
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            static_path=os.path.join(os.path.dirname(__file__), "static"),
            ui_modules=uimodule.modulelist,
            xsrf_cookies=True,
            cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
            login_url="/404",
            debug=False,
            default_handler_class=DefaultHandler,
            lasttime_rss_update=0,
        )

        # Parse config file and command line
        if os.path.exists(settings["config_dir"]) and os.path.isfile(settings["config_file"]):
            config.set_settings(settings)
        else:
            print("config file not found, exit")
            sys.exit(0)

        tornado.web.Application.__init__(self, urls , **settings)

        try:
            # Have one global connection to the blog DB across all handlers
            self.db = mytorndb.Connection(
                host     = config.options.mysql_host, 
                database = config.options.mysql_database,
                user     = config.options.mysql_user, 
                password = config.options.mysql_password
            )
        except Exception as e:
            loggingg.info("mysql connection error: " + e)


def main():
    signal.signal(signal.SIGINT, signal_handler)
    http_server = tornado.httpserver.HTTPServer(Application())

    # only allow access from localhost when debug is False
    http_server.listen(config.options.port, address= \
        '' if config.options.debug else '127.0.0.1')

    logging.info("Listening on port %d" % config.options.port)
    tornado.ioloop.IOLoop.instance().start()

def signal_handler(signal, frame):
    print("\b\bCtrl-C.... Exiting")
    sys.exit(0)

if __name__ == "__main__":
    main()
