from flask import Flask, flash, request, Response, redirect, abort, render_template
import pandas as pd
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import requests

response = requests.get("http://grtcbustracker.com/bustime/api/v3/getvehicles?key=<'API ACCESS KEY'>&rt=BRT,1A,2A,3A&format=json")
df = pd.DataFrame.from_dict(response.json()['bustime-response']['vehicle'])

app = Flask(__name__)

dash_app = dash.Dash(
    __name__,
    server=app,
    url_base_pathname='/dash/'
)

dash_app.layout = html.Div([
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Buses in Service', children=[
            html.Div(children=[
                html.H1(children='GRTC Route Info'),

                html.Div(children='''
                Number of Buses in Service
                 '''),

                dcc.Graph(id='graph'),
                dcc.Interval(
                    id='interval-component',
                    interval=7200*1000, # in milliseconds
                    n_intervals=0
                 )
            ])
        ]),
        dcc.Tab(label='Vehicles in Service - Details', children=[
            dash_table.DataTable(
                id='table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data = [])
        ])
    ])
])

@dash_app.callback(
    [Output('graph', 'figure'),
     Output('table', 'data')],
    [Input('interval-component', 'n_intervals')])
def update_figure(n):
    response = requests.get("http://grtcbustracker.com/bustime/api/v3/getvehicles?key=<'API ACCESS KEY'>&rt=BRT,1A,2A,3A&format=json")
    df = pd.DataFrame.from_dict(response.json()['bustime-response']['vehicle'])
    rtname = []
    rtnum = []
    for x in df.rt.unique():
        rtnum.append(len(df.loc[df['rt'] == x]))
    for x in df.rt.unique():
        rtname.append(x)
    data=df.to_dict('records')
    return {
            'data': [
                {'x': rtname, 'y': rtnum, 'type': 'bar', 'name': 'number of buses per route'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }, data





if __name__ == '__main__':
    app.run()
