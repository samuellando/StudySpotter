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

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server


# Plotly mapbox public token
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"


# map api request
#r = requests.get('http://35.232.203.137', auth=('user', 'pass'))
#y = r.json()

with open('locations.json') as json_file:
    y = json.load(json_file)

# map generation variables
names = []
lats = []
lngs = []
densities = []
ids =  []
new_zoom = 12
new_latitude = 45.507553
new_longitude = -73.578129

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
    dropdown_options.append({'label': location['name'], 'value': json.dumps({'id' : location['id'], 'lat' : location['lat'], 'lng' : location['lng']}) })

    # LAYOUT

app.layout = html.Div(
    children=[
        html.Div(
            className="row",
            children=[
                # Column for user controls
                html.Div(
                    className="four columns div-user-controls",
                    children=[
                        html.H1("StudySpotter"),
                        # searchbar
                        html.Div([
                            dcc.Dropdown(
                                id = 'search-dropdown',
                                options=dropdown_options,
                                placeholder= "Select a Library",
                            )
                        ], style={
                        }), 
                        # sidebar
                        html.Div(id='sidebar', style = {'overflow-y': 'auto', 'height' : '80vh', 'margin' : "0 auto", 'scrollbar-color' : 'dark'})
                     ],
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

    # FUNCTIONS

def srequest_from_id(srequest_id):
    #specific_view_request = requests.get('http://35.232.203.137?location=' + srequest_id , auth=('user', 'pass'))
    #specific_view_obj = specific_view_request.json()
    with open('data.json') as json_file:
      specific_view_obj = json.load(json_file)[srequest_id]

    # parsing JSON for specific view
    loc_name = specific_view_obj['name']
    loc_description = "'"+specific_view_obj['dsc']+"'"
    loc_businness = float(densities[ids.index(srequest_id)])
    if loc_businness < 20:
        business_level = "empty"
    elif 20 <= loc_businness and loc_businness < 40:
        business_level = "chillaxed"
    elif 40 <= loc_businness and loc_businness < 60:
        business_level = "lively"
    elif 60 <= loc_businness and loc_businness < 80:
        business_level = "busy"
    else:
        business_level = "hellish"

    graphs = [
        html.Div(children=[html.H1(loc_name), html.P(loc_description), html.P(">"+business_level, style = {"font-style" : "italic"})])
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
                            'color': 'white'
                        },
                        'showlegend': False,
                        'title' : label_name,
                        'yaxis':{
                             'title':'Density'
                        },

                    },
                },
                style={'height': 300}
            )
        )
        # print(graphs)
    return graphs

    # CALLBACK EVENTS

# search bar callback event
@app.callback(Output(component_id='map', component_property='figure'), [Input(component_id='search-dropdown', component_property='value')])
def goto_location(selected_value):
    if selected_value:
        selected_value_dict = json.loads(selected_value)
        new_zoom = 15
        new_latitude = float(selected_value_dict['lat'])
        new_longitude = float(selected_value_dict['lng'])
    else :
        new_zoom = 12.3
        new_latitude = 45.494477
        new_longitude = -73.585914

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
@app.callback(Output(component_id='sidebar', component_property='children'), [Input("map", "clickData"), Input(component_id='search-dropdown', component_property='value')])
def update_selected_data(clickData, selected_value):
    if clickData:
        requestID = ids[clickData['points'][0]['pointIndex']]
        return srequest_from_id(requestID)

    elif selected_value:
        selected_value_dict = json.loads(selected_value)
        return srequest_from_id(selected_value_dict['id'])

    else : #default landing thing
        return [
            html.P("Some study spaces are more full than others, but which one is more full? Good question! Our app can show and predict how busy the libraries are, and make recommendations based on real time and predicted population densities. So people can better use the spaces. ", style = {'padding-top' : '14px'}),
        ]

if __name__ == "__main__":
    app.run_server(debug=True)
