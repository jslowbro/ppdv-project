# -*- coding: utf-8 -*-
import json

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

from domain import models_marshaller
from services import historic_data_collector, historic_data_service, tesla_service, utils

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

# static values
client_id = 1
reload_time = 500
max_length = 1000

color_map = {
    'l0': '#2c8129',
    'l1': '#cbe927',
    'l2': '#6eddaa',
    'r0': '#fe9882',
    'r1': '#ff6201',
    'r2': '#cd2701',
    'L0': '#2c8129',
    'L1': '#cbe927',
    'L2': '#6eddaa',
    'R0': '#fe9882',
    'R1': '#ff6201',
    'R2': '#cd2701'
}

# ON Start
historic_data_collector.start_collecting_historic_data()

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    # Hidden div inside the app that stores the intermediate value
    html.Div(id='trace-state', style={'display': 'none'}),
    html.Div(id='person-state', style={'display': 'none'}),
    html.Div(id='historic-readings-state', style={'display': 'none'}),
    ######
    # INTERVALS
    dcc.Interval(
        id='interval-component',
        interval=1 * reload_time,
        n_intervals=0
    ),
    ###########
    html.H1(children='Welcome to Walking Visualiser',
            style={
                'textAlign': 'center'
            }),
    html.Div([
        html.Div(children=[
            html.Label('Choose a person'),
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
                            html.Th(children='Is the person disabled ?')
                        ]),
                        html.Tr(id='person-data')
                    ])

                ]
            ),

        ]),
        html.Figure(children=[
            html.Img(src='/assets/feet.png',
                     style={'textAlign': 'center'}
                     ),
            html.Figcaption('Sensors placement on feet'),
        ],
            style={'textAlign': 'center'}
        ),
    ], style={'columnCount': 2}),
    html.H2(children='Live Walking View',
            style={
                'textAlign': 'center'
            }),
    dcc.Graph(
        id='example-graph',
        animate=True
    ),
    html.H2(children='Historic Data Viewer',
            style={
                'textAlign': 'center'
            }),
    dcc.Graph(id='historic-data-graph'),
    html.Div([
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
            value=['l0', 'l1', 'l2'],
            labelStyle={'display': 'inline-block'}
        ),
        html.Button(
            'Refresh Historic Values',
            id='refresh-historic-data',
            n_clicks=0
        ),
    ], style={'textAlign': 'center'}),
    html.Div(
        [
            html.H6(id='range-slider-label'),
        ], style={'textAlign': 'center'}
    ),
    dcc.RangeSlider(
        id='historic-data-slider',
        min=0,
        max=3600,
        step=1,
        value=[0, 10],
        allowCross=False
    ),
    html.H2(children='Anomaly Screener',
            style={
                'textAlign': 'center'
            }),
    dcc.Graph(id='anomaly-viewer'),
    html.Div([
        html.Div([
            dcc.Checklist(
                id='anomaly-sensor-checklist',
                options=[
                    {'label': 'L0', 'value': 'l0'},
                    {'label': 'L1', 'value': 'l1'},
                    {'label': 'L2', 'value': 'l2'},
                    {'label': 'R0', 'value': 'r0'},
                    {'label': 'R1', 'value': 'r1'},
                    {'label': 'R2', 'value': 'r2'}
                ],
                value=['l0', 'l1', 'l2'],
                labelStyle={'display': 'inline-block'}
            ),
        ]),
        html.Div([
            dcc.Dropdown(
                id='anomaly-dropdown',
                options=[]
            ),
        ]),
    ], style={'textAlign': 'center', 'margin': '10px'}),
])


@app.callback(
    Output('anomaly-viewer', 'figure'),
    [Input('anomaly-dropdown', 'value'), Input('anomaly-sensor-checklist', 'value')]
)
def update_anomaly_graph(anomaly_trace_json, sensor_options):
    if anomaly_trace_json is None:
        return {}
    anomaly_trace = json.loads(anomaly_trace_json)
    traces = anomaly_trace['traces']
    return {
        'data': [
            dict(
                x=[i for i in range(0, len(traces))],
                y=[i[s] for i in traces],
                name=s,
                mode='lines+markers',
                type='scatter',
                marker={
                    'color': color_map[s]
                },
                showlegend=False
            ) for s in sensor_options
        ],
        'layout': {
            'title': 'Trace in which an anomaly has been detected',
            'xaxis': {'title': 'Timeline of data points'},
            'yaxis': {'title': 'Pressure on sensor'},
            'font': {
                'size': 8
            }
        },
    }


@app.callback(
    Output('anomaly-dropdown', 'options'),
    [Input('person-dropdown', 'value'), Input('refresh-historic-data', 'n_clicks')]
)
def load_anomaly_dropdown(patient_id, n_clicks):
    anomalies = historic_data_service.get_anomalies_for_patient(patient_id)
    options = [{'label': a.anomaly_start[0:19] + ' - ' + a.anomaly_end[0:19], 'value': json.dumps(a.__dict__)} for a in
               anomalies]
    return options


@app.callback(
    Output('example-graph', 'figure'),
    Input('trace-state', 'children')
)
def update_graph_live(reading_json):
    reading = models_marshaller.reading_from_json(reading_json)
    return {
        'data': [
            dict(
                x=[sensor.name],
                y=[sensor.value],
                type='bar',
                marker={
                    'color': color_map[sensor.name]
                },
                showlegend=False
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
    Output('historic-readings-state', 'children'),
    [Input('refresh-historic-data', 'n_clicks'), Input('person-dropdown', 'value')]
)
def save_historic_trace_to_state(n_clicks, patient_id):
    traces = list(map(lambda t: t.__dict__, historic_data_service.get_traces(patient_id)))
    traces_json = json.dumps(traces)
    return traces_json


@app.callback(
    [Output('historic-data-slider', 'max'), Output('historic-data-slider', 'marks')],
    Input('historic-readings-state', 'children')
)
def update_slider(historic_readings_state):
    historic_readings = list(json.loads(historic_readings_state))
    max_range = len(historic_readings)
    marks = utils.generate_marks(max_range)
    return max_range, marks


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
        html.Td(children=str(reading.disabled))
    ]


@app.callback(
    Output('historic-data-graph', 'figure'),
    [Input('sensor-checklist', 'value'),
     Input('historic-data-slider', 'value'),
     Input('historic-readings-state', 'children')]
)
def display_historic_readings_graph(sensor_options, slider_range, historic_readings_state):
    traces = list(json.loads(historic_readings_state))[slider_range[0]:slider_range[1]]
    return {
        'data': [
            dict(
                x=[i for i in range(slider_range[0], slider_range[1])],
                y=[i[s] for i in traces],
                name=s,
                mode='lines+markers',
                type='scatter',
                marker={
                    'color': color_map[s]
                },
                showlegend=False,
            ) for s in sensor_options
        ],
        'layout': {
            'title': 'View historic traces, maximum of 10 minutes backwards',
            'xaxis': {'title': 'Timeline of data points'},
            'yaxis': {'title': 'Pressure on sensor'},
            'font': {
                'size': 8
            }
        },
    }


@app.callback(
    Output('range-slider-label', 'children'),
    Input('historic-data-slider', 'value')
)
def display_range_slider_value(slider_range):
    return 'You are viewing an interval : {} - {}'.format(slider_range[0], slider_range[1])


if __name__ == '__main__':
    app.run_server(debug=True)
