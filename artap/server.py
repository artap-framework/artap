import dash
import dash_core_components as dashComp
import dash_html_components as dashHtml
from dash.dependencies import Input, Output
import plotly.graph_objs as grObj

import webbrowser
import socket
from threading import Thread
import time

from jedi._compatibility import pickle_dump

from artap.enviroment import Enviroment
# from .individual import Individual

class NoneProblemDefined(Exception):
    """Raised when no problem instance is given

    Attributes:
        message -- explanation of exception
    """

    def __init__(self, message):
        self.message = message


class RunDashThread(Thread):

    def __init__(self, dash_app, debug_mode, url, port):
        Thread.__init__(self)
        self.dash_app = dash_app
        self.debug_mode = debug_mode
        self.url = url
        self.port = port

    def run(self):
        self.dash_app.run_server(debug=self.debug_mode, host=self.url, port=self.port)


class ArtapServer(Thread):

    def __init__(self, problem=None, local_host=True, port=Enviroment.server_initial_port, graph_update_interval=100, debug_mode=False):
        if problem is None:
            raise NoneProblemDefined('No problem was given')
        Thread.__init__(self)

        self.problem = problem

        if local_host:
            self.url = Enviroment.loopback_ip
        else:
            self.url = self.get_host_ip()

        self.port = port
        self.debug_mode = debug_mode

        self.keep_server_live = True

        self.x = []
        self.y = []
        self.data = []
        self.last_population = 0

        external_stylesheets = ['mainstyle.css']
        self.dash_app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

        # local css
        html_colors = {
            'background': '#000099',
            'text': '#e6f9ff'
        }
        self.dash_app.layout = dashHtml.Div(style={'backgroundColor': html_colors['background']}, children=[
            dashHtml.H1(
                id='page_title',
                children='Artap Server',
                style={
                    'textAlign': 'center',
                    'color': html_colors['text']
                }
            ),
            dashHtml.H2(
                id='stop_info',
                children='',
                style={
                    'textAlign': 'center',
                    'color': html_colors['text']
                }
            ),
            dashComp.Graph(
                id='live-update-graph',
                figure={
                    'data': [grObj.Scatter(
                        {
                            'x': self.x,
                            'y': self.y,
                            'mode': 'markers',
                            'opacity': 0.7,
                            'marker': {
                                'size': len(self.problem.data_store.populations) * 2,
                                'line': {'width': 0.5, 'color': 'white'},
                                'color': len(self.problem.data_store.populations)
                            },
                            'name': 'Pareto {}'.format(len(self.problem.data_store.populations))
                        }
                    )],
                    'layout': grObj.Layout(
                        xaxis={'title': str(self.problem.eval_counter)},
                        yaxis={'title': str(self.problem.costs)}
                    )
                }
            ),
            dashComp.Interval(
                id='interval-component',
                interval=graph_update_interval,  # in milliseconds
                n_intervals=0
            ),
            dashHtml.Button('Stop Server', id='stop-button'),
            dashHtml.Div(id='output-button-container')
        ])

        @self.dash_app.callback(Output('stop_info', 'children'),
                                [Input('stop-button', 'n_clicks')])
        def cancel_server(number_of_clicks):
            if number_of_clicks is not None:
                self.stop_server()
                return dashHtml.Div([
                    dashHtml.Div('Artap Server was STOPPED'),
                ])

        # Multiple components can update everytime interval gets fired.
        @self.dash_app.callback(Output('live-update-graph', 'figure'),
                                [Input('interval-component', 'n_intervals')])
        def update_graph_live(n):
            print('update_graph_live - self.problem.data_store.populations: {}'.format(len(self.problem.data_store.populations)))

            if self.last_population != len(self.problem.data_store.populations):
                self.x = []
                self.y = []
                population = self.problem.data_store.populations[-1]
                for individual in population.individuals:
                    # self.x.append(len(self.x))
                    if individual.front_number == 1:
                        self.x.append(individual.costs[0])
                        self.y.append(individual.costs[1])

                # print(self.x)
                # print(self.y)

                trace = grObj.Scatter(
                        {
                            'x': self.x,
                            'y': self.y,
                            'mode': 'markers',
                            'opacity': 0.7,
                            'marker': {
                                'size': len(self.problem.data_store.populations) * 2,
                                'line': {'width': 0.5, 'color': 'white'},
                                'color': len(self.problem.data_store.populations)
                            },
                            'name': 'Pareto {}'.format(len(self.problem.data_store.populations))
                        }
                    )

                self.data.append(trace)
                self.last_population = len(self.problem.data_store.populations)
            fig = {
                'data': self.data,
                'layout': grObj.Layout(
                    xaxis={'title': str(self.problem.eval_counter)},
                    yaxis={'title': str(self.problem.costs)}
                )
            }
            return fig

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
        # self.dash_app.run_server(debug=self.debug_mode, host=self.url, port=self.port)
        run_dash = RunDashThread(self.dash_app, self.debug_mode, self.url, self.port)
        run_dash.setDaemon(daemonic=True)
        run_dash.start()

        while self.keep_server_live:
            time.sleep(Enviroment.server_keep_live_delay)

    def run_server(self, open_viewer=True, daemon=True):
        self.setDaemon(daemonic=daemon)
        self.start()

        if open_viewer:
            # webbrowser.register('google-chrome', webbrowser.Chrome('google-chrome'))
            webbrowser.open_new(self.url + ':' + str(self.port))

    def stop_server(self):
        self.keep_server_live = False


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
