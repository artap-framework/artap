import dash
import dash_core_components as dashComp
import dash_html_components as dashHtml
from dash.dependencies import Input, Output
import plotly.graph_objs as grObj

import numpy as np
import pandas as pd
import os

x = np.linspace(0, 5, 50)
y = np.sin(x)


app = dash.Dash(__name__)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

# app.layout = dashHtml.Div()

app.layout = dashHtml.Div([
    dashComp.Graph(
        id='live-update-graph',
        figure={
            'data': [grObj.Scatter(
                {
                    'x': x,
                    'y': y,
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
@app.callback(Output('live-update-graph', 'figure'),
              [Input('interval-component', 'n_intervals')])
def update_graph_live(n):
    x = np.linspace(0, 5, 50)
    y = np.sin(x * n) / n
    print(n)
    dummy_data = pd.read_csv('testdata.csv')
    print(dummy_data)

    fig = {
            'data': [grObj.Scatter(
                {
                    'x': x,
                    'y': y,
                    'name': 'Trace 1'
                }
            )],
            'layout': grObj.Layout(
                xaxis={'title': dummy_data.to_string()},
                yaxis={'title': dummy_data.to_string()}
            )
        }
    return fig


if __name__ == '__main__':
    #app.run_server(debug=False, host='147.228.96.138', port=8050)
    app.run_server(debug=True)
