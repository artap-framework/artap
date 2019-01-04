import json
from textwrap import dedent as d

import dash
import dash_core_components as dashComp
import dash_html_components as dashHtml
from dash.dependencies import Input, Output
import plotly.graph_objs as grObj

import numpy as np

x = np.linspace(0, 5, 50)
y = np.sin(x)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = dashHtml.Div([
    dashComp.Graph(
        id='basic-interactions',
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

    dashHtml.Div(className='row', children=[
        dashHtml.Div([
            dashComp.Markdown(d("""
                **Hover Data**

                Mouse over values in the graph.
            """)),
            dashHtml.Pre(id='hover-data', style=styles['pre'])
        ], className='three columns'),

        dashHtml.Div([
            dashComp.Markdown(d("""
                **Click Data**

                Click on points in the graph.
            """)),
            dashHtml.Pre(id='click-data', style=styles['pre']),
        ], className='three columns'),

        dashHtml.Div([
            dashComp.Markdown(d("""
                **Selection Data**

                Choose the lasso or rectangle tool in the graph's menu
                bar and then select points in the graph.
            """)),
            dashHtml.Pre(id='selected-data', style=styles['pre']),
        ], className='three columns'),

        dashHtml.Div([
            dashComp.Markdown(d("""
                **Zoom and Relayout Data**

                Click and drag on the graph to zoom or click on the zoom
                buttons in the graph's menu bar.
                Clicking on legend items will also fire
                this event.
            """)),
            dashHtml.Pre(id='relayout-data', style=styles['pre']),
        ], className='three columns')
    ])
])


@app.callback(
    Output('hover-data', 'children'),
    [Input('basic-interactions', 'hoverData')])
def display_hover_data(hoverData):
    return json.dumps(hoverData, indent=2)


@app.callback(
    Output('click-data', 'children'),
    [Input('basic-interactions', 'clickData')])
def display_click_data(clickData):
    return json.dumps(clickData, indent=2)


@app.callback(
    Output('selected-data', 'children'),
    [Input('basic-interactions', 'selectedData')])
def display_selected_data(selectedData):
    return json.dumps(selectedData, indent=2)


@app.callback(
    Output('relayout-data', 'children'),
    [Input('basic-interactions', 'relayoutData')])
def display_selected_data(relayoutData):
    return json.dumps(relayoutData, indent=2)


if __name__ == '__main__':
    app.run_server(debug=True)