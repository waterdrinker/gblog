import tornado.web

from gblog import utils
from gblog.basehandler import BaseHandler


class CommentHandler(BaseHandler):
    """Handle URL '/comment'.

    Subclass of BaseHandler and RequestHandler, 
    support standard GET/POST method.
    """

    def get(self):
        """GET method. Render comments html."""

        try:
            entry_id = self.get_argument("id", None)
        except tornado.web.MissingArgumentError:
            raise tornado.web.HTTPError(500)

        try:
            int(entry_id)
        except ValueError:
            raise tornado.web.HTTPError(500)

        comments = self.db.query("SELECT * FROM comments WHERE \
                entry_id={0}".format(entry_id))
       
        reply_map={}
        i=0
        for comment in comments:
            reply_map[ comment["id"] ]=i
            i+=1

        self.render("modules/comments.html", comments=comments, entry_id=entry_id, reply_map=reply_map)

    def post(self):
        """ POST method. Receive submitted comment.

        Receive a submitted comment, store in database,
        And return the comment in html.
        """

        # Get arguments from POST
        entry_id = self.get_argument("id", None)
        author = self.get_argument("author")
        email = self.get_argument("email")
        content = self.get_argument("content")
        
        # if not reply any comment, reply_id will be ''
        try:
            reply_id = self.get_argument("reply_id")
        except tornado.web.MissingArgumentError:
            reply_id = 0
        
        try:
            url = self.get_argument("url")
        except tornado.web.MissingArgumentError:
            url = ''

        if not url:
            url = 'javascript:void(0);'
        else:
            url = utils.get_url(url)
        if not reply_id: reply_id = 0

        try:
            entry_id = int(entry_id)
            reply_id = int(reply_id)
        except ValueError:
            raise tornado.web.HTTPError(500)

        # format content
        content=utils.format_comment_content(content)

        # Update comments cnt
        self.db.execute("UPDATE entries SET comments=comments+1 WHERE \
                id = {0}".format(entry_id))

        # Check replied_comment existed
        if reply_id > 0:
            replied_comment = self.db.get("SELECT * FROM comments WHERE id = {0}".format(reply_id))
            if not replied_comment:
                replied_comment = {'author': 'unknown', 'url':'javascript:void(0);', 'content': 'This comment has been deleted'}
                reply_id = -1
        else:
            replied_comment = None

        author=utils.escape_text(author)
        content=utils.escape_text(content)
        # Insert into database
        comment_id = self.db.execute("INSERT INTO comments(entry_id,reply_id,published, \
                author,email,url,content) VALUES({id},{rp},UTC_TIMESTAMP(),\
                '{nm}', '{em}', '{ur}', '{ct}')".format(id=entry_id, rp=reply_id,
                nm=author, em=email, ur=url, ct=content))

        self.render("modules/comments_item.html", comment={'author':author, 'url':url, 
            'content':content, 'published':None, 'id':comment_id, 'entry_id':entry_id, 'reply_id':reply_id}, replied_comment=replied_comment)


    @tornado.web.authenticated
    def delete(self):
        """DELETE method. 
        
        Delete a comment, need authentication.
        """

        comment_id=self.get_argument("id", None)
        entry_id=self.get_argument("entry_id", None)

        if not comment_id or not entry_id: 
            raise tornado.web.HTTPError(500)

        try:
            int(comment_id)
            int(entry_id)
        except ValueError:
            raise tornado.web.HTTPError(500)


        # Check comments relations
        self.db.execute("UPDATE comments SET reply_id = -1 WHERE reply_id  = {0}".format(comment_id))

        # Delete comment from database
        self.db.execute("DELETE FROM comments WHERE id = {0}".format(comment_id))

        # Update 'comments' from database
        self.db.execute("UPDATE entries SET comments=IF(comments<1, 0, comments-1) WHERE id = {0}".format(entry_id))

