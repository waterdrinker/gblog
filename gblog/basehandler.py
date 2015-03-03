import tornado.web
import tornado.options


class BaseHandler(tornado.web.RequestHandler):
    @property
    def db(self):
        return self.application.db

    # override to determine the current user from the cookie
    def get_current_user(self):
        user_id = self.get_secure_cookie("blogdemo_user")
        if not user_id: return None
        return self.db.get("SELECT * FROM authors WHERE id = {0}".format(int(user_id)))

    #def write_error(self):
        #self.render("sjkdflhsa")


    def write_error(self, status_code, **kwargs):
        """Override to implement custom error pages.

        ``write_error`` may call `write`, `render`, `set_header`, etc
        to produce output as usual.

        If this error was caused by an uncaught exception (including
        HTTPError), an ``exc_info`` triple will be available as
        ``kwargs["exc_info"]``.  Note that this exception may not be
        the "current" exception for purposes of methods like
        ``sys.exc_info()`` or ``traceback.format_exc``.
        """
        self.render("error.html", code=status_code, message=self._reason)
