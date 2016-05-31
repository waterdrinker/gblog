import os
import time
import calendar
import logging
import tornado

from gblog import config
from gblog import utils 
from gblog.handlers.basehandler import BaseHandler



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
        xml_path = self.settings["rss_xml_path"]
        if(now - self.settings["rss_update_time"] > 86400):
            logging.info("update RSS feed")
            self.settings["rss_update_time"] = now
            timestr = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(now))
            xml = self.render_string("feed.xml", entries=entries, update_time= \
                    timestr)

            try:
                # write xml bytes to xml_path
                with open(xml_path, "wb") as f:
                    f.write(xml)
            except Exception as e:
                logging.info("write xml_path failed: %s" % e)

            f.close()

            self.write(xml)
            return
        
        # if xml_path file exist
        if os.path.isfile(xml_path):
            f = open(xml_path, "r")
            self.write(f.read())
            f.close()
        else:
            timestr = time.strftime("%a, %d %b %Y %H:%M:%S +0000", time.gmtime(
                      self.settings["rss_update_time"]))
            self.render("feed.xml", entries=entries, update_time=timestr)


