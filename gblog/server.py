import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.escape
import signal
import sys
import logging

import gblog.handlers as handlers
from gblog import mytorndb
from gblog import config
from gblog import uimodule


class Application(tornado.web.Application):
    def __init__(self):
        urls = [
            (r"/", handlers.HomeHandler),
            (r"/about", handlers.AboutHandler),
            (r"/archive", handlers.ArchiveHandler),
            (r"/feed", handlers.FeedHandler),
            (r"/entry/([^/]+)", handlers.EntryHandler),
            (r"/comment", handlers.CommentHandler),
            (r"/compose", handlers.ComposeHandler),
            (r"/auth/login", handlers.AuthLoginHandler),
            (r"/auth/google", handlers.GoogleOAuth2LoginHandler),
            (r"/auth/logout", handlers.AuthLogoutHandler),
            (r"/category", handlers.CategoryHandler),
            (r"/proxy/supervisor(.*)", handlers.ProxySuperHandler),
            (r"/supervisor", handlers.SuperHandler),
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
            default_handler_class=handlers.DefaultHandler,
            rss_update_time=0,
            rss_xml_path = "/var/www/http/feed.xml",
        )

        tornado.web.Application.__init__(self, urls, **settings)

    # Parse config file and command line
    def init_settings(self):
        if os.path.exists(self.settings["config_dir"]) and \
        os.path.isfile(self.settings["config_file"]):
            config.get_options(self.settings)
        else:
            logging.error("config file not found")
            return False

        if not self.settings["debug"]:
            for i in self.handlers:
                if(i[0] == r"/auth/login"):
                    self.handlers.remove(i)
        return True

    def init_db(self):
        # Have one global connection to the blog DB across all handlers
        self.db = mytorndb.Connection(
            host     = config.options.mysql_host,
            database = config.options.mysql_database,
            user     = config.options.mysql_user,
            password = config.options.mysql_password
        )

        if not self.db._db:
            logging.error("mysql connection error")
            return False

        return True


def main():
    app = Application()
    if not app.init_settings() or not app.init_db():
        logging.info("Exiting")
        sys.exit(0)

    if config.options.debug:
        signal.signal(signal.SIGINT, signal_handler)

    http_server = tornado.httpserver.HTTPServer(app)

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
