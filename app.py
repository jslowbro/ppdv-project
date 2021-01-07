# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# to install things run this command in your command line:
# pip install package_name
# Example : pip install dash


# In this file we have our main application which creates a webserver available on http://localhost:8050.
# This file is responsible for generating dynamic dash graphs and other components.
# It asks tesla_service.py and historic_data_service.py to fetch data and then displays that data in dash components
# It also handles user interactions like user checking a box or choosing an option from a dropdown menu

import models_marshaller
import tesla_service
from historic_data_service import get_traces, start_collecting_historic_data, fetch_and_save_trace

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# static values
client_id = 1
reload_time = 500
max_length = 1000

# ON Start
start_collecting_historic_data()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(children=[
    # Hidden div inside the app that stores the intermediate value
    html.Div(id='trace-state', style={'display': 'none'}),
    html.Div(id='person-state', style={'display': 'none'}),
    ######
    # INTERVALS
    dcc.Interval(
        id='interval-component',
        interval=1 * reload_time,
        n_intervals=0
    ),
    dcc.Interval(
        id='historic-data-interval',
        interval=1 * 2000,
        n_intervals=0
    ),
    ###########
    html.H1(children='Welcome to walking simulation',
            style={
                'textAlign': 'center',
                'color': 'blue'
            }),
    html.Label('Dropdown'),
    dcc.Dropdown(
        id='person-dropdown',
        options=[
            {'label': 'Janek Grzegorczyk', 'value': 1},
            {'label': u'Elżbieta Kochalska', 'value': 2},
            {'label': 'Albert Lisowski', 'value': 3},
            {'label': 'Ewelina Nosowska', 'value': 4},
            {'label': 'Piotr Fokalski', 'value': 5},
            {'label': 'Bartosz Moskalski', 'value': 6}
        ],
        value=client_id
    ),
    dcc.Graph(
        id='example-graph',
        animate=True
    ),
    html.Table(
        style={
            'width': "100%"
        },
        children=[
            html.Thead(children=[
                html.Tr(children=[
                    html.Th(children='First name'),
                    html.Th(children='Last name'),
                    html.Th(children='Birth Date'),
                    html.Th(children='Is the person disabled ?'),
                    html.Th(children='Trace comment')
                ]),
                html.Tr(id='person-data')
            ])

        ]
    ),
    html.H3(children='Choose sensors to view historic values'),
    dcc.Checklist(
        id='sensor-checklist',
        options=[
            {'label': 'L0', 'value': 'l0'},
            {'label': 'L1', 'value': 'l1'},
            {'label': 'L2', 'value': 'l2'},
            {'label': 'R0', 'value': 'r0'},
            {'label': 'R1', 'value': 'r1'},
            {'label': 'R2', 'value': 'r2'}
        ],
        value=['L0', 'L1', 'L2'],
        labelStyle={'display': 'inline-block'}
    ),
    html.Button(
        'Refresh Historic Values',
        id='refresh-historic-data',
        n_clicks=0
    ),
    dcc.Graph(id='historic-data-graph', animate=True)

])


@app.callback(
    Output('example-graph', 'figure'),
    Input('trace-state', 'children')
)
def update_graph_live(reading_json):
    reading = models_marshaller.reading_from_json(reading_json)
    return {
        'data': [
            dict(
                x=[sensor.id],
                y=[sensor.value],
                name=sensor.name,
                type='bar'
            ) for sensor in reading.trace.sensors
        ],
        'layout': {
            'title': 'Simulation of a walking process',
            'transition': {'duration': reload_time / 5},
            'font': {
                'size': 8
            }
        }
    }


@app.callback(
    Output('trace-state', 'children'),
    [Input('interval-component', 'n_intervals'), Input('person-dropdown', 'value')]
)
def save_reading_to_state(n_intervals, person_id):
    reading = tesla_service.get_patient_reading(person_id)
    reading_json = reading.toJSON()
    return reading_json


@app.callback(
    Output('person-state', 'children'),
    Input('person-dropdown', 'value')
)
def save_person_to_state(person_id):
    reading = tesla_service.get_patient_reading(person_id)
    reading_json = reading.toJSON()
    return reading_json


@app.callback(
    Output('person-data', 'children'),
    Input('person-state', 'children')
)
def get_person_from_state(reading_json):
    reading = models_marshaller.reading_from_json(reading_json)
    return [
        html.Td(children=reading.firstname),
        html.Td(children=reading.lastname),
        html.Td(children=reading.birthdate),
        html.Td(children=str(reading.disabled)),
        html.Td(children=reading.trace.name)
    ]


@app.callback(
    Output('historic-data-graph', 'figure'),
    [Input('person-dropdown', 'value'),
     Input('sensor-checklist', 'value'),
     Input('historic-data-interval', 'n_intervals')]
)
def display_historic_readings_graph(patient_id, sensor_options, n_intervals):
    traces = map(lambda t: t.__dict__, get_traces(patient_id))
    print(len(traces))
    return {
        'data': [
            dict(
                x=[i for i in range(0, len(traces) - 1)],
                y=[i[s] for i in traces],
                name=s
            ) for s in sensor_options
        ],
        'layout': {
            'title': 'View of sensor specific trace',
            'font': {
                'size': 8
            }
        },
    }


if __name__ == '__main__':
    app.run_server(debug=True)
