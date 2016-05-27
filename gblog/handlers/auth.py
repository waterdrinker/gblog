import os.path
import tornado
import tornado.auth

from gblog import config
from gblog import utils 
from gblog.handlers.basehandler import BaseHandler


class GoogleOAuth2LoginHandler(BaseHandler, 
        tornado.auth.GoogleOAuth2Mixin):
    """Handle URL '/auth/login'

    """

    @tornado.gen.coroutine
    def get(self):

        if self.get_current_user():
            self.redirect("/")

        if self.get_argument('code', False):
            access = yield self.get_authenticated_user(
                    redirect_uri='http://gongyusong.com/auth/google',
                    code=self.get_argument('code'))
            user = yield self.oauth2_request(
                    "https://www.googleapis.com/oauth2/v1/userinfo",
                    access_token=access["access_token"])

            # BEGIN: process the user
            if not user:
                raise tornado.web.HTTPError(500, "Google auth failed")

            author = self.db.get("SELECT * FROM authors WHERE email = \
                    '{0}'".format(user["email"]))

            if not author:
                # Auto-create first author
                author_exist = self.db.get("SELECT * FROM authors LIMIT 1")
                if not author_exist:
                    author_id = self.db.execute( "INSERT INTO authors \
                            (email,name,admin) VALUES ('{0}','{1}',1)".format(
                                user["email"], user["name"]))
                else:
                    author_id = self.db.execute( "INSERT INTO authors \
                            (email,name,admin) VALUES ('{0}','{1}',0)".format(
                                user["email"], user["name"]))

            self.set_secure_cookie("user", user["email"])
            self.redirect(self.get_argument("next", "/"))   #登陆失败 跳转到next

            # END: process the user

        else:
            yield self.authorize_redirect(
                    redirect_uri='http://gongyusong.com/auth/google',
                    client_id=self.settings['google_oauth']['key'],
                    scope=['profile', 'email'],
                    response_type='code',
                    extra_params={'approval_prompt':'auto'})


class AuthLoginHandler(BaseHandler):
    def get(self):

        if self.get_current_user():
            self.redirect("/")

        if not self.settings["debug"]:
            raise tornado.web.HTTPError(404)

        self.write('<html><body><form action="/auth/login" method="post">'
                   'Name: <input type="text" name="name">'
                   '<input type="submit" value="sign in">'
                   '<input type="hidden" name="_xsrf" value="%s"/>'
                   '</form></body></html>' % self.xsrf_token.decode())
        
    def post(self):
        user = self.get_argument("name")

        self.set_secure_cookie("user", self.get_argument("name"))
        self.redirect("/")


class AuthLogoutHandler(BaseHandler):
    """Handle URL '/auth/logout'

    """

    def get(self):
        self.clear_cookie("user")
        self.redirect(self.get_argument("next", "/"))

