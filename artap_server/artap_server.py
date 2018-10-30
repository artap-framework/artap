import cherrypy

from artap.enviroment import Enviroment
from templates import WebPagesWriter


class ArtapServer(object):

    def __init__(self):
        self.static_dir = Enviroment.artap_root + "../artap_server/static/"
        self.writer = WebPagesWriter()

    @cherrypy.expose
    def index(self):
        file = open(self.static_dir + 'index.html', 'r')
        page = file.readlines()

        return page

    @cherrypy.expose
    def problems(self):
        html_page = self.writer.problems()
        return html_page

    @cherrypy.expose
    def calculation(self, id=None):
        html_page = self.writer.calculation_details(id)
        return html_page

    @cherrypy.expose
    def problem(self, id=None):
        html_page = self.writer.problem_details(id)
        return html_page

    # only for first plotly library tests
    @cherrypy.expose
    def plotly(self):
        file = open(Enviroment.artap_root + "../artap_server/static/plotly/plotlytest.html", 'r')
        html_page = file.readlines()
        return html_page

    @cherrypy.expose
    def plotly2(self):
        file = open(Enviroment.artap_root + "../artap_server/static/plotly/plotlytest2.html", 'r')
        html_page = file.readlines()
        return html_page


if __name__ == '__main__':

    static_dir = Enviroment.artap_root + "../artap_server/"
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': static_dir
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': static_dir + 'static/'
        }
    }
    cherrypy.config.update({'server.socket_host': '127.0.0.1',
                        'server.socket_port': 8080,
                       })
    cherrypy.quickstart(ArtapServer(), '/', conf)