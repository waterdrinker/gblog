import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import tornado.escape

from gblog import mytorndb
from gblog import config
from gblog import handlers
from gblog import compose
from gblog import comment
from gblog import uimodule

settings = dict(
    blog_title="example's Blog",
    blog_url="example.com",
    config_dir_path=os.path.expanduser('~') + '/.gblog',
    template_path=os.path.join(os.path.dirname(__file__), "templates"),
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    ui_modules=uimodule.modulelist,
    xsrf_cookies=True,
    cookie_secret="__TODO:_GENERATE_YOUR_OWN_RANDOM_VALUE_HERE__",
    login_url="/auth/login",
    debug=True,
    default_handler_class=handlers.DefaultHandler,
)

class Application(tornado.web.Application):
    def __init__(self):
        urls = [
            (r"/", handlers.HomeHandler),
            (r"/about", handlers.AboutHandler),
            (r"/archive", handlers.ArchiveHandler),
            (r"/feed", handlers.FeedHandler),
            (r"/entry/([^/]+)", handlers.EntryHandler),
            (r"/comment", comment.CommentHandler),
            (r"/compose", compose.ComposeHandler),
            (r"/auth/login", handlers.AuthLoginHandler),
            (r"/auth/logout", handlers.AuthLogoutHandler),
            (r"/category", handlers.CategoryHandler),
            (r"/(favicon.ico)", tornado.web.StaticFileHandler, {"path": "/static"}),
        ]
        tornado.web.Application.__init__(self, urls , **settings)

        # Have one global connection to the blog DB across all handlers
        self.db = mytorndb.Connection(
            host     = config.options.mysql_host, 
            database = config.options.mysql_database,
            user     = config.options.mysql_user, 
            password = config.options.mysql_password
        )


def main():

    config_file_path = settings["config_dir_path"] + '/gblog.conf'
    if os.path.isfile(config_file_path): 
        tornado.options.parse_config_file(config_file_path)
        settings["blog_title"]=config.options.blog_title
        settings["blog_url"]=config.options.blog_url
    else:
        print("Cannot find the configure file")

    tornado.options.parse_command_line();

    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(config.options.port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
