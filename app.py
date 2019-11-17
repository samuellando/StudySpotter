import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import numpy as np

from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt

import json
import requests
print('das')
app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"


# map api request
r = requests.get('http://35.232.203.137', auth=('user', 'pass'))
y = r.json()

# map generation variables
names = []
lats = []
lngs = []
densities = []
ids =  []
new_zoom = 12
new_latitude = 45.507553
new_longitude = -73.578129

# colors baby
colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# specific view generation vars

time_axis = [
    "01:00", "01:30", 
    "02:00", "02:30", 
    "03:00", "03:30", 
    "04:00", "04:30", 
    "05:00", "05:30", 
    "06:00", "06:30", 
    "07:00", "07:30", 
    "08:00", "08:30", 
    "09:00", "09:30", 
    "10:00", "10:30", 
    "11:00", "11:30", 
    "12:00", "12:30", 
    "13:00", "13:30", 
    "14:00", "14:30", 
    "15:00", "15:30", 
    "16:00", "16:30", 
    "17:00", "17:30", 
    "18:00", "18:30", 
    "19:00", "19:30", 
    "20:00", "20:30", 
    "21:00", "21:30", 
    "22:00", "22:30", 
    "23:00", "23:30", 
    "24:00", "24:30", 
]

# dropdown array
dropdown_options = []

#get data from json 
for location in y['locations']:
    names.append(location['name'])
    lats.append(float(location['lat']))
    lngs.append(float(location['lng']))
    densities.append(int(location['density']))
    ids.append(location['id'])
    dropdown_options.append({'label': location['name'], 'value': location['lat'] + "," + location['lng']})

    # LAYOUT

app.layout = html.Div(
    children=[
        # searchbar
        html.Div([
            dcc.Dropdown(
                id = 'search-dropdown',
                options=dropdown_options,
                placeholder= "Select a Library",
            )
        ], style={
            'position' : 'absolute',
            'z-index' : '2',
            'width' : '30vw',
            'margin' : '10px 10px 10px 10px'
        }), 
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[ html.Div(id='sidebar', style = {'overflow-y': 'auto', 'height' : '85vh'})],
                ),
                # Column for app graphs and plots
                html.Div(
                    className="eight columns div-for-charts bg-grey",
                    children=[
                        dcc.Graph(
                            id = "map",  
                            style={"height":"100vh", "width": "100%", "z-index" : 4},
                        ),
                    ],
                ),
            ],
        )
    ]
)

    # CALLBACK EVENTS

# search bar callback event
@app.callback(Output(component_id='map', component_property='figure'), [Input(component_id='search-dropdown', component_property='value')])
def goto_location(selected_value):
    if selected_value:
        new_zoom = 15
        selected_value_list = selected_value.split(",")
        print(selected_value_list)
        new_latitude = float(selected_value_list[0])
        new_longitude = float(selected_value_list[1])
    else :
        new_zoom = 12
        new_latitude = 45.507553
        new_longitude = -73.578129

    return go.Figure(
        data=[  
            Scattermapbox(
                lat=lats,
                lon=lngs,
                mode="markers",
                hoverinfo="text",
                text=names,
                marker= go.scattermapbox.Marker(
                    size=10,
                    cmin = 0,
                    cmax = 100,
                    showscale=False,
                    color = densities,
                    colorscale= [[0, 'rgb(0,255,0)'], [1, 'rgb(255,0,0)']],

                    #opacity=0.3,
                    # symbol = 'circle',
                ),
            )
        ],
        
        layout=Layout(
            autosize=True,
            margin=go.layout.Margin(l=0, r=0, t=0, b=0),
            showlegend=False,
            mapbox=dict(
                accesstoken=mapbox_access_token,
                center=dict(lat=new_latitude, lon=new_longitude), # A new Location
                style="dark",
                bearing=0,
                zoom=new_zoom,
            )
        )
    )

# map marker click callback event
@app.callback(Output(component_id='sidebar', component_property='children'), [Input("map", "clickData")])
def update_selected_data(clickData):
    if clickData != None:
        requestID = ids[clickData['points'][0]['pointIndex']]
        specific_view_request = requests.get('http://35.232.203.137?location=' + requestID , auth=('user', 'pass'))
        specific_view_obj = specific_view_request.json()

        # parsing JSON for specific view
        loc_name = specific_view_obj['name']
        loc_description = specific_view_obj['dsc']

        graphs = [
            html.Div(children=[html.H1(loc_name), html.H4(loc_description)], style = {'color' : colors['text'], 'margin' : '0px 0px 0px 0px', 'font-family' : ' Arial', 'padding' : '10px 10px 10px 10px'})
        ]
        for label in specific_view_obj['labels']:
            label_name = label
            label_data = specific_view_obj['labels'][label]['data']
            label_avg = specific_view_obj['labels'][label]['avg']
            graphs.append(
                dcc.Graph(
                    figure={
                        'data': [
                            {'x': time_axis, 'y': label_data, 'type': 'bar', 'name': 'Current'},
                            {'x': time_axis, 'y': label_avg, 'type': 'line', 'name': 'Avg'},
                        ],
                        'layout': {
                            'plot_bgcolor': 'rgba(0,0,0,0)',
                            'paper_bgcolor': 'rgba(0,0,0,0)',
                            'font': {
                                'color': colors['text']
                            },
                            'showlegend': False,
                            'title' : label_name
                        },
                    },
                    style={'height': 300}
                )
            )
            # print(graphs)
        return graphs

    else : #default landing thing
        return [
            html.H1("StudySpotter")
        ]

if __name__ == "__main__":
    app.run_server(debug=True)
