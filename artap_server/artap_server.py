# import os

from flask import Flask

# from artap.enviroment import Enviroment


class ArtapServer(Flask):

    def __init__(self, name):
        super(ArtapServer, self).__init__(name)


if __name__ == '__main__':
    app = ArtapServer(__name__)

    @app.route("/")
    def hello():
        return "<br /><br />Welcome to Artap server based on Python Flask!<br /><br />Only to test if Flask works..."

    app.run()