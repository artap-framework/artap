import dash
import dash_core_components as dashComp
import dash_html_components as dashHtml
from dash.dependencies import Input, Output
import plotly.graph_objs as grObj

import webbrowser
import socket
from threading import Thread

import numpy as np
import pandas as pd


class ArtapServer(Thread):

    def __init__(self, local_host=True, port=8050, debug_mode=False):
        Thread.__init__(self)

        if local_host:
            self.url = '127.0.0.1'
        else:
            self.url = self.get_host_ip()

        self.port = port
        self.debug_mode = debug_mode

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
                interval=1 * 1000,  # in milliseconds
                n_intervals=0
            )
        ])

        # Multiple components can update everytime interval gets fired.
        @self.dash_app.callback(Output('live-update-graph', 'figure'),
                      [Input('interval-component', 'n_intervals')])
        def update_graph_live(n):
            self.y = np.sin(self.x * n) / n
            dummy_data = pd.read_csv('testdata.csv')

            fig = {
                'data': [grObj.Scatter(
                    {
                        'x': self.x,
                        'y': self.y,
                        'name': 'Trace 1'
                    }
                )],
                'layout': grObj.Layout(
                    xaxis={'title': dummy_data.to_string()},
                    yaxis={'title': dummy_data.to_string()}
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
            return socket.gethostbyname(socket.gethostname())
        except:
            return None

    def run(self):
        self.dash_app.run_server(debug=self.debug_mode, host=self.url, port=self.port)

    def run_server(self, open_viewer=True):
        self.setDaemon(daemonic=True)
        self.start()

        if open_viewer:
            webbrowser.open(self.url + ':' + str(self.port), new=2, autoraise=True)


if __name__ == '__main__':
    # for debug testing only
    artap_server = ArtapServer(local_host=True, port=8050, debug_mode=False)
    artap_server.run_server()

    artap_server_2 = ArtapServer(local_host=True, port=8051, debug_mode=False)
    artap_server_2.run_server()

    input("Press Enter to STOP application...")
