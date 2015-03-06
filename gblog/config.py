
from tornado.options import define, options

define("blog_url", default='localhost', help="your site domain")
define("port", default=8888, help="run on the given port", type=int)
define("entries_per_page", default=5, help="pagination", type=int)

define("blog_title", default="gblog", help="blog name")
define("description", default="blogging about stuffs", help="blog name")
define("mysql_host", default="127.0.0.1:3306", help="blog database host")
define("mysql_database", default="blog", help="blog database name")
define("mysql_user", default="blog", help="blog database user")
define("mysql_password", default="blog", help="blog database password")

define("cookie_secret", default="cNOsNilqQli9f8wXR4lT6LXatHmAdUhShYCrCAihHDc=")
