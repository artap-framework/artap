import os, os.path
import random
import string
import cherrypy
from artap.datastore import SqliteDataStore

class ArtapServer(object):
    @cherrypy.expose
    def index(self):
        file = open('artap_server/static/index.html','r')
        page = file.readlines()

        return page

    @cherrypy.expose
    def problems(self):
        file = open('artap_server/static/problem.html','r')
        #page = string.Template(file.readlines())
        #html_page = page.substitute(content = "Neco")
        html_page = file.readlines()
        return html_page

    @cherrypy.expose
    def generate(self, length=8):
        some_string = ''.join(random.sample(string.hexdigits, int(length)))
        cherrypy.session['mystring'] = some_string
        return some_string

    @cherrypy.expose
    def display(self):
        return cherrypy.session['mystring']


if __name__ == '__main__':
    print(os.getcwd())
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'artap_server/static'
        }
    }
    cherrypy.config.update({'server.socket_host': '127.0.0.1',
                        'server.socket_port': 8080,
                       })
    cherrypy.quickstart(ArtapServer(), '/', conf)