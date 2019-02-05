import dash
import dash_core_components as dashComp
import dash_html_components as dashHtml
from dash.dependencies import Input, Output
import plotly.graph_objs as grObj

import webbrowser
import socket
from threading import Thread

import os

from artap.enviroment import Enviroment

import numpy as np
import pandas as pd

class NoneProblemDefined(Exception):
    """Raised when no problem instance is given

    Attributes:
        message -- explanation of exception
    """

    def __init__(self, message):
        self.message = message


class ArtapServer(Thread):

    def __init__(self, problem=None, local_host=True, port=Enviroment.server_initial_port, debug_mode=False):
        if problem is None:
            raise NoneProblemDefined('No problem was given')

        Thread.__init__(self)

        if local_host:
            self.url = Enviroment.loopback_ip
        else:
            self.url = self.get_host_ip()

        self.port = port
        self.debug_mode = debug_mode

        # DEBUG
        print(problem.costs)
        print(problem.eval_counter)
        # -----

        self.__x = np.linspace(0, 5, 500)
        self.__y = np.sin(self.__x)

        self.__dash_app = dash.Dash(__name__)

        self.__dash_app.layout = dashHtml.Div([
            dashComp.Graph(
                id='live-update-graph',
                figure={
                    'data': [grObj.Scatter(
                        {
                            'x': self.x,
                            'y': self.y,
                            'name': 'Trace 1',
                        }
                    )]
                }
            ),
            dashComp.Interval(
                id='interval-component',
                interval=1 * 100,  # in milliseconds
                n_intervals=0
            )
        ])

        # Multiple components can update everytime interval gets fired.
        @self.dash_app.callback(Output('live-update-graph', 'figure'),
                      [Input('interval-component', 'n_intervals')])
        def update_graph_live(n):
            # DEBUG
            print(problem.costs)
            print(problem.eval_counter)
            # -----

            self.y = np.sin(self.x * n) / n
            # dummy_data = pd.read_csv('testdata.csv')
            fig = {
                'data': [grObj.Scatter(
                    {
                        'x': self.x,
                        'y': self.y,
                        'name': 'Trace 1'
                    }
                )],
                'layout': grObj.Layout(
                    xaxis={'title': str(problem.eval_counter)},
                    yaxis={'title': str(problem.costs)}
                )
            }
            return fig

    @property
    def x(self):
        """ 'x' property."""
        return self.__x

    @x.setter
    def x(self, value):
        self.__x = value

    @property
    def y(self):
        """ 'y' property."""
        return self.__y

    @y.setter
    def y(self, value):
        self.__y = value

    @property
    def dash_app(self):
        """ 'dash_app' property."""
        return self.__dash_app

    def get_host_ip(self):
        try:
            return ((([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or
                      [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in
                        [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0])
        except:
            return Enviroment.loopback_ip

    # need to be tested, if it is correct
    def pick_unused_port(self, ip_addr=Enviroment.loopback_ip):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((ip_addr, 0))
        addr, port = s.getsockname()
        s.close()
        return port

    def run(self):
        self.dash_app.run_server(debug=self.debug_mode, host=self.url, port=self.port)

    def run_server(self, open_viewer=True, daemon=True):
        self.setDaemon(daemonic=daemon)
        self.start()

        if open_viewer:
            # webbrowser.register('google-chrome', webbrowser.Chrome('google-chrome'))
            webbrowser.open_new(self.url + ':' + str(self.port))


if __name__ == '__main__':
    # for debug testing only
    from artap.tests.test_problem_scipy import AckleyN2Problem
    problem = AckleyN2Problem('DummyProblem')
    port = Enviroment.server_initial_port
    try:
        artap_server = ArtapServer(local_host=True, port=port, debug_mode=False)
        artap_server.run_server()
        port += 1
    except NoneProblemDefined as ex:
        print('Exception when start server 1: ', ex.message)

    try:
        artap_server_2 = ArtapServer(problem=problem, local_host=True, port=port, debug_mode=False)
        artap_server_2.run_server()
        port += 1
    except NoneProblemDefined as ex:
        print('Exception when start server 2: ', ex.message)

    try:
        artap_server_3 = ArtapServer(problem=problem, local_host=True, port=port, debug_mode=False)
        artap_server_3.run_server()
    except NoneProblemDefined as ex:
        print('Exception when start server 3: ', ex.message)

    input("Press Enter to STOP application...")
