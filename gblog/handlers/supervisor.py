import logging
import tornado.httpclient
import tornado.web

from gblog import utils
from gblog.handlers.basehandler import BaseHandler


class ProxySuperHandler(BaseHandler):
    """Handle URL '/super'.
    proxy for supervisord

    """

    @tornado.web.authenticated
    def get(self, url):
        self.is_admin()
        request = self.request
        query = '?' + request.query if request.query else ''
        URI = 'http://127.0.0.1:9001' + url + query

        #new_request = tornado.httpclient.HTTPRequest(URI)
        #new_request.method = request.method
        #new_request.headers = request.headers

        http_client = tornado.httpclient.HTTPClient()
        try:
            #response = http_client.fetch(new_request)
            response = http_client.fetch(URI)
        except Exception as e:
            logging.info("http_client get response error: %s" % e)
            self.write("Can't access to the supervisorctl server")
            self.finish()
            return
        
        for i in response.headers:
            self.set_header(i, response.headers[i])

        self.write(response.body)

    def post(self):
        logging.info("get POST request")
        return


class SuperHandler(BaseHandler):
    """Handle URL '/supervisor'.
    proxy for supervisord

    """
    
    @tornado.web.authenticated
    def get(self):
        self.is_admin()
        self.render("supervisor.html")


