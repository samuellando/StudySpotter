import datetime

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import pandas as pd
import numpy as np
import json
import requests

import plotly.graph_objects as go
from dash.dependencies import Input, Output
from dash.dependencies import Input, Output
from plotly import graph_objs as go
from plotly.graph_objs import *
from datetime import datetime as dt

app = dash.Dash(
    __name__, meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)
server = app.server
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"

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


app.layout = html.Div(className = "row", children=[
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
    
    # Creating the map element
    dcc.Graph(
        id = "map",  
        style={"height":"100vh", "width": "100%"}
    ),

    html.Div(id='my-div'),

    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(x=names, y=densities, marker=dict(color="blue"), hoverinfo="x")
            ]
        )
    ),

])

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
@app.callback(Output(component_id='my-div', component_property='children'), [Input("map", "clickData")])
def update_selected_data(clickData):
    if clickData != None:
        requestID = ids[clickData['points'][0]['pointIndex']]
        specific_view_request = requests.get('http://35.232.203.137?location=' + requestID , auth=('user', 'pass'))
        specific_view_obj = specific_view_request.json()

        # parsing JSON for specific view
        loc_name = specific_view_obj['name']
        loc_description = specific_view_obj['dsc']
        for label in specific_view_obj['labels']:
            label_name = label
            label_data = specific_view_obj['labels'][label]['data']
            label_avg = specific_view_obj['labels'][label]['avg']
            # TODO: PLOT GRAPH FOR THIS LABEL


    return ""


if __name__ == '__main__':
    app.run_server(debug=True)
