import os
import time
import calendar
import logging
import tornado

from gblog import config
from gblog import utils 
from gblog.handlers.basehandler import BaseHandler

xml_path = "/var/www/http/feed.xml"


class FeedHandler(BaseHandler):
    """Handle URL '/feed'.

    Subclass of BaseHandler and RequestHandler, support standard GET.
    """

    def get(self):

        entries = self.db.query("SELECT * FROM entries ORDER BY \
                published DESC LIMIT 10")
        self.set_header("Content-Type", "application/atom+xml")

        # get the seconds since epoch
        now = calendar.timegm(time.gmtime())
        if(now - self.settings["lasttime_rss_update"] > 86400):
            logging.info("update RSS feed")
            self.settings["lasttime_rss_update"] = now
            timestr = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(now))
            xml = self.render_string("feed.xml", entries=entries,
                    update_time=timestr)

            try:
                # write xml bytes to xml_path
                with open(xml_path, "wb") as f:
                    f.write(xml)
            except Exception as e:
                logging.info("write xml_path failed: %s" % e)
                f.close()
            f.close()

            self.write(xml)
            return
        
        if os.path.exists(self.settings["config_dir"]):
            f = open(xml_path, "r")
            self.write(f.read())
            f.close()
        else:
            timestr = time.strftime("%a, %d %b %Y %H:%M:%S +0000", 
                    time.gmtime(self.settings["lasttime_rss_update"]))
            self.render("feed.xml", entries=entries,
                    update_time=self.settings["lasttime_rss_update"])


