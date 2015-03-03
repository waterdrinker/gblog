import os.path
import tornado
import tornado.auth
import markdown

from gblog.basehandler import BaseHandler
from gblog import config
from gblog import utils 




class HomeHandler(BaseHandler):
    """Handle URL '/'.

    Subclass of BaseHandler and RequestHandler, support standard GET/POST method.
    """

    def get(self):
        """Return the home page."""
        # Calculate the pages num
        entries_per_page=config.options.entries_per_page  
        try:
            int(entries_per_page)
        except ValueError:
            raise tornado.web.HTTPError(500)

        count = self.db.get("SELECT COUNT(*) FROM entries")
        count = list(count.values())[0]
        pages = int((count-1)/entries_per_page + 1)  # equal math.ceil(a/b)
        pages = pages if pages else 1  # pages cannot be 0


        entries = self.db.query("SELECT id,title,slug,abstract,published,readtimes,comments FROM entries ORDER BY \
                published DESC LIMIT {0}".format(entries_per_page))
        if not entries:
            pass
        tags_list = self.db.query("SELECT * FROM tags")
        dates_list = self.db.query("SELECT * FROM dates")
        self.render("home.html", entries=entries, tags_list=tags_list, dates_list=dates_list, pages=pages)

    def post(self):
        """Return the entries in home page #."""
        page = self.get_argument("page", None)
        if not page: raise tornado.web.HTTPError(404)
        entries_per_page=config.options.entries_per_page  
        start = int(page)*entries_per_page - entries_per_page
        entries = self.db.query("SELECT id,title,slug,abstract,published,readtimes,comments FROM entries ORDER BY \
                published DESC LIMIT {0},{1}".format(start, entries_per_page))
        self.render("modules/entry.html", entries=entries)


class AboutHandler(BaseHandler):
    """Handle URL '/about'.
    """
    def get(self): 
        """Return the about page."""
        about_file_path = self.settings["config_dir_path"] + '/about.md'
        if os.path.isfile(about_file_path): 
            f = open(about_file_path)
            content=f.read()
            content = markdown.markdown(content)
        else:
            content = None

        comments = self.db.query("SELECT * FROM comments WHERE \
                entry_id={0}".format(0))
       
        #if comments:
        reply_map={}
        i=0
        for comment in comments:
            reply_map[ comment["id"] ]=i
            i+=1
        self.render("about.html", content=content, comments=comments, entry_id=0, reply_map=reply_map)


class DefaultHandler(BaseHandler):
    """handler of default_handler_class in Application Setting.

    """

    def get(self):
        """Return the 404 page."""
        self.render("404.html")


class EntryHandler(BaseHandler):
    """Handle URL '/entry/[^/]+'.

    Subclass of BaseHandler and RequestHandler, support standard GET method.
    """

    def get(self, slug):
        entry = self.db.get("SELECT * FROM entries WHERE slug = '{0}'"\
                .format(slug))
        if not entry: raise tornado.web.HTTPError(404)

        # Update readtimes
        if not self.current_user:
          entry.readtimes+=1
          self.db.execute( "UPDATE entries SET readtimes = '{0}' WHERE \
                  id = {1}".format(entry.readtimes, entry.id))

        tags_list = self.db.query("SELECT * FROM tags")
        dates_list = self.db.query("SELECT * FROM dates")

        # Query the pre and next article
        query = self.db.query("(SELECT id,slug,title FROM entries WHERE id<{0} ORDER BY id DESC LIMIT 1) UNION ALL (SELECT id,slug,title FROM entries WHERE id>{0} ORDER BY id LIMIT 1)".format(entry.id))
        # Only little interger can use 'is'
        if len(query) is 2:
            pre = query[0]
            nex = query[1]
        elif len(query) is 1:
            if query[0]["id"] < entry["id"]:
                pre = query[0]
                nex = None
            else:
                pre = None
                nex = query[0]
        else:
            pre = None
            nex = None

        self.render("article.html", entry=entry, tags_list=tags_list, dates_list=dates_list, pre=pre, nex=nex)


class ArchiveHandler(BaseHandler):
    """Handle URL '/archive'.

    Subclass of BaseHandler and RequestHandler, support standard GET method.
    """

    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY \
                published DESC")
        self.render("archive.html", entries=entries)


class CategoryHandler(BaseHandler):
    """Handle URL '/category'.
    
    """
    def get(self):
        # Check argument
        name=self.get_argument("name")
        id = self.get_argument("id")
        
        # Check id
        try:
            int(id)
        except ValueError:
            raise tornado.web.HTTPError()

        if name == "tag":
            entries = self.db.query("SELECT * FROM entries WHERE id IN (SELECT entry_id FROM tagmaps WHERE tag_id = {0})".format(id))
            if not entries:
                raise tornado.web.HTTPError(404)
            tag = self.db.get("SELECT * FROM tags WHERE id = {0} LIMIT 1".format(id))
            self.render("category.html", entries=entries, category="tag", item=tag)
        elif name == "date":
            entries = self.db.query("SELECT * FROM entries WHERE id IN (SELECT entry_id FROM datemaps WHERE date_id = {0})".format(id))
            if not entries:
                raise tornado.web.HTTPError(404)
            date = self.db.get("SELECT * FROM dates WHERE id = {0} LIMIT 1".format(id))
            self.render("category.html", entries=entries, category="date", item=date)

        else:
            raise tornado.web.HTTPError(404)
        


class FeedHandler(BaseHandler):
    """Handle URL '/feed'.

    Subclass of BaseHandler and RequestHandler, support standard GET/POST method.
    """

    def get(self):
        entries = self.db.query("SELECT * FROM entries ORDER BY \
                published DESC LIMIT 10")
        self.set_header("Content-Type", "application/atom+xml")
        self.render("feed.xml", entries=entries)


class AuthLoginHandler(BaseHandler, tornado.auth.GoogleMixin):
    """Handle URL '/auth/login'

    """

    @tornado.web.asynchronous
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


class AuthLogoutHandler(BaseHandler):
    """Handle URL '/auth/logout'

    """

    def get(self):
        self.clear_cookie("blogdemo_user")
        self.redirect(self.get_argument("next", "/"))
