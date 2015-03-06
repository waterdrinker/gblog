import tornado.options
from tornado.options import define, options


# Settings available to handlers
define("blog_title",       default="gblog", help="blog name")
define("blog_url",         default='127.0.0.1', help="your site domain")
define("cookie_secret",    default="cNOsNilqQli9f8wXR4lT6LXatHmAdUhShYCrCAihHDc=")
define("debug",            default=False, type=bool)
define("description",      default="blogging about stuffs", help="blog name")

# Settings available only in tornado.options
define("port",             default=8888, help="run on the given port", type=int)
define("entries_per_page", default=5, help="pagination", type=int)
define("mysql_host",       default="127.0.0.1:3306", help="blog database host")
define("mysql_database",   default="blog", help="blog database name")
define("mysql_user",       default="blog", help="blog database user")
define("mysql_password",   default="blog", help="blog database password")


def set_settings(settings):
    try:
        config_file_path = settings["config_dir_path"] + '/gblog.conf'
        #if os.path.isfile(config_file_path):
        tornado.options.parse_config_file(config_file_path)
        tornado.options.parse_command_line()
    except:
        print("Parse configure FAILED")
        raise

    settings["blog_title"]    = options.blog_title
    settings["blog_url"]      = options.blog_url
    settings["cookie_secret"] = options.cookie_secret
    settings["debug"]         = options.debug
    settings["description"]   = options.description

