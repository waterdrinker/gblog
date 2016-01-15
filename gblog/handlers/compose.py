import re
from datetime import date
import tornado.web

from gblog import utils
from gblog.handlers.basehandler import BaseHandler


def delete_tags(tagstring, db, entry_id):
    """Clean the datatable tags and tagmaps."""

    # Clean tagmaps
    if entry_id:
        db.execute("DELETE FROM tagmaps WHERE entry_id = {0}".format(entry_id))

    # Clean tags
    tags=tagstring.split(',')
    for tag in tags:
        db.execute("UPDATE tags SET cnt = IF(cnt<1, 0, cnt-1) WHERE name = '{0}' LIMIT 1".format(tag))
    db.execute("DELETE FROM tags WHERE cnt = 0")


class ComposeHandler(BaseHandler):
    """Handle URL '/compose'.

    Subclass of BaseHandler and RequestHandler, support standard GET/POST method.
    """

    @tornado.web.authenticated
    def get(self):
        """Return the article edit page."""
        self.is_admin()

        id = self.get_argument("id", None)

        # Check id
        try:
            if id: 
                int(id)
                entry = self.db.get("SELECT * FROM entries WHERE id = {0}".format(id))
            else:
                entry = None
        except ValueError:
            raise tornado.web.HTTPError(500)

        self.render("compose.html", entry=entry)


    @tornado.web.authenticated
    def post(self):
        """Handle user input and write to database."""
        self.is_admin()

        entry_id    = self.get_argument("id", None)
        title = self.get_argument("title")
        tags  = self.get_argument("tags")
        text  = self.get_argument("markdown")

        # escape for python braces and mysql quote in string
        tags = utils.escape_text(tags)
        # Check id
        try:
            if entry_id: int(entry_id)
        except ValueError:
            raise tornado.web.HTTPError(500)

        if(len(title) > 512): title = title[0:512]

        # prune the oversize of the tags 
        if tags: tags = utils.get_tags(tags)
        else: tags = 'untagged'
        if(len(tags) > 100): tags = tags[0:100]
        
        # Get the html and abstract:
        #text = tornado.escape.xhtml_escape(text)
        (html,abstract) = utils.get_html_abstract(text, size=120)

        # escape for python braces and mysql quote in string
        # do after markdown solve
        text = utils.escape_text(text)
        html = utils.escape_text(html)
        abstract = utils.escape_text(abstract)

        # Case 1. Insert entry first time
        if not entry_id:
            # prune the oversize of the slug, title
            slug = utils.get_nice_slug(title)
            if not slug: slug = "entry"
            if(len(slug) > 100): slug = slug[0:100]

            # Make sure the slug is unique:
            while True:
                dup = self.db.get("SELECT * FROM entries WHERE slug = '{0}'"\
                        .format(slug))
                if not dup: break
                slug += "-2"
            # Insert the entry:
            entry_id = self.db.execute(
                 "INSERT INTO entries (author_id,title,slug,tags, \
                 markdown,html,abstract,published,readtimes,comments) VALUES ({au},'{ti}','{sl}',\
                 '{tg}','{md}','{ht}','{ab}',UTC_TIMESTAMP(),0,0)".format(au=
                 self.current_user.id, ti=title, sl=slug, tg=tags,
                 md=text, ht=html, ab=abstract))
                
            # Insert date category
            today = date.today()
            datecate='{:04}-{:02}'.format(today.year, today.month)
            any_date = self.db.get("SELECT id FROM dates where name = '{0}' LIMIT 1".format(datecate))
            if any_date:
                date_id = any_date["id"]
                self.db.execute("UPDATE dates SET cnt=cnt+1 WHERE id = {0}".format(date_id))
            else:
                date_id = self.db.execute("INSERT INTO dates (name, cnt) VALUES ('{0}', 1)".format(datecate))
            self.db.execute("INSERT INTO datemaps (date_id, entry_id) VALUES ({0}, {1})".format(date_id, entry_id))

        # Case 2. Entry already exist
        else:
            # Get the existed entry's tags
            existed_entry = self.db.get("SELECT tags,slug FROM entries WHERE id = {0} LIMIT 1".format(entry_id))
            if not existed_entry: raise tornado.web.HTTPError(404)
            slug=existed_entry["slug"] 
            # Clean the datatable tags and tagmaps:
            delete_tags(existed_entry["tags"], self.db, entry_id); 
            
            # Update the entry:
            # Dont change the slug
            self.db.execute(
                "UPDATE entries SET title = '{ti}', \
                 tags = '{tg}', markdown = '{md}', html = '{ht}', abstract='{ab}'\
                 WHERE id = {i}".format(ti=title,  tg=tags,
                     md=text, ht=html, ab=abstract, i=entry_id))
                

        # Tags insert for all cases
        tags=tags.split(',')
        # Make the element in tags UNIQUE:
        tags={}.fromkeys(tags).keys()
        for tag in tags:
            if(len(tag)>20): tag=tag[0:20]
            # If the tag existed, update it's cnt:
            any_tag = self.db.get("SELECT * FROM tags WHERE name = '{0}' LIMIT 1".format(tag))
            if any_tag:
                tag_id = any_tag["id"]
                self.db.execute("UPDATE tags SET cnt = cnt+1 WHERE id = {0}".format(tag_id))
            else:
                tag_id = self.db.execute("INSERT INTO tags (name, cnt) VALUES ('{0}', 1)".format(tag))
            self.db.execute("INSERT INTO tagmaps (tag_id, entry_id) VALUES ({0}, {1})".format(tag_id, entry_id))

        # Redirect:
        self.redirect("/entry/" + slug)

    @tornado.web.authenticated
    def delete(self):
        """ DELETE article:
        delete comments,
        update tags,
        update dates category.
        """
        self.is_admin()

        entry_id = self.get_argument("entry_id")

        if entry_id:
            del_entry = self.db.get("SELECT tags FROM entries WHERE id = {0} LIMIT 1".format(entry_id))
        
        # Update tags
        delete_tags(del_entry["tags"], self.db, entry_id)
        
        # Upadate dates category
        if entry_id:
            datemap = self.db.get("SELECT date_id FROM datemaps where entry_id = {0} LIMIT 1".format(entry_id))
            self.db.execute("DELETE FROM datemaps where entry_id = {0} LIMIT 1".format(entry_id))
        if datemap:
            self.db.execute("UPDATE dates SET cnt = IF(cnt<1, 0, cnt-1) WHERE id = {0} LIMIT 1".format(datemap["date_id"]))
        self.db.execute("DELETE FROM dates WHERE cnt = 0 LIMIT 1")

        # delete comments
        if entry_id:
            self.db.execute("DELETE FROM comments where entry_id = {0}".format(entry_id))

        # delete article
        if entry_id:
            self.db.execute("DELETE FROM entries where id = {0} LIMIT 1".format(entry_id))
