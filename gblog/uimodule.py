import tornado


class EntryModule(tornado.web.UIModule):
    def render(self, entries):
        return self.render_string("modules/entry.html", entries=entries)


class SidebarModule(tornado.web.UIModule):
    def render(self, tags_list, dates_list, entry_id):
        return self.render_string("modules/sidebar.html", tags_list=tags_list,
                dates_list=dates_list, entry_id=entry_id)


class PagenavModule(tornado.web.UIModule):
    def render(self, pages):
        return self.render_string("modules/pagenav.html", pages=pages)


class CommentsModule(tornado.web.UIModule):
    def render(self, comments, entry_id, reply_map):
        return self.render_string("modules/comments.html", comments=comments,entry_id=entry_id,reply_map=reply_map)


class CommentsItemModule(tornado.web.UIModule):
    def render(self, comment, replied_comment=None):
        return self.render_string("modules/comments_item.html", comment=comment, replied_comment=replied_comment)


class CommentsPostModule(tornado.web.UIModule):
    def render(self, entry_id):
        return self.render_string("modules/comments_post.html", entry_id=entry_id)


modulelist = {"Entry":    EntryModule, 
              "Sidebar": SidebarModule,
              "Pagenav":  PagenavModule,
              "Comments": CommentsModule,
              "CommentsItem": CommentsItemModule,
              "CommentsPost": CommentsPostModule
              }
