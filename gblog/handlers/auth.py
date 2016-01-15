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
        if self.get_argument("code", False):
            user = yield self.get_authenticated_user(
                    redirect_uri='http://gongyusong.com/auth/google',
                    code=self.get_argument('code'))
        else:
            yield self.authorize_redirect(
                    redirect_uri='http://gongyusong.com',
                    client_id=self.settings['google_oauth']['key'],
                    scope=['profile', 'email'],
                    response_type='code',
                    extra_params={'approval_prompt':'auto'})


    """                
class AuthLoginHandler(BaseHandler, tornado.auth.GoogleOAuth2Mixin):

    def get(self):
        if self.get_argument("openid.mode", None):
            self.get_authenticated_user(self._on_auth)
            return
        self.authenticate_redirect()

    def _on_auth(self, user):
        if not user:
            raise tornado.web.HTTPError(500, "Google auth failed")
        author = self.db.get("SELECT * FROM authors WHERE email = \
                '{0}'".format(user["email"]))
        if not author:
            # Auto-create first author
            any_author = self.db.get("SELECT * FROM authors LIMIT 1")
            if not any_author:
                author_id = self.db.execute( "INSERT INTO authors \
                        (email,name) VALUES ('{0}','{1}')".format(
                            user["email"], user["name"]))
            else:
                self.redirect("/")  #认证失败
                return
        else:
            #self.redirect("/entry")
            author_id = author["id"]    #用户存在，设置author_id作为其cookie
        self.set_secure_cookie("blogdemo_user", str(author_id))
        self.redirect(self.get_argument("next", "/"))   #登陆失败 跳转到next
    """

class AuthLoginHandler(BaseHandler):
    def get(self):
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

