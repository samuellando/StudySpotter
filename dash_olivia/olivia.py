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
    __name__
)
server = app.server
mapbox_access_token = "pk.eyJ1IjoicGxvdGx5bWFwYm94IiwiYSI6ImNqdnBvNDMyaTAxYzkzeW5ubWdpZ2VjbmMifQ.TXcBE-xg9BFdV2ocecc_7g"
list_of_locations = {
    "Trottier": {"lat": 45.507553,"lon": -73.578995},
    "Webster Library": {"lat": 45.497355,"lon": -73.578129},
}



#json_test = '{"id" : "0", "name": "Trottier Building", "lat": 45.507603, "lon" : -73.578973, "density" : 71}'

#print(y["id"])
#response.content


r = requests.get('http://35.232.203.137', auth=('user', 'pass'))
y = r.json()

names = []
lats = []
lngs = []
densities = []
ids =  []

for location in y['locations']:
    names.append(location['name'])
    lats.append(float(location['lat']))
    lngs.append(float(location['lng']))
    densities.append(int(location['density']))
    ids.append(location['id'])

app.layout = html.Div([
    html.Div([
        dcc.Dropdown(
            options=[
                {'label': 'McGill Trottier', 'value': 'mcgilltrotier'},
                {'label': 'Concordia EV', 'value': 'concordiaev'},
            ],
            placeholder="Select a Library",
        )
    ]), 
    
    
    dcc.Graph(
        id = "map",
        figure=go.Figure(
            data=[  
                Scattermapbox(
                    lat=lats,
                    lon=lngs,
                )
            ],
            
            layout=Layout(
                autosize=True,
                margin=go.layout.Margin(l=0, r=35, t=0, b=0),
                showlegend=False,
                mapbox=dict(
                    accesstoken=mapbox_access_token,
                    center=dict(lat=list_of_locations["Trottier"]["lat"], lon=list_of_locations["Trottier"]["lon"]),  # 40.7272  # -73.991251
                    style="dark",
                    bearing=0,
                    zoom=12,
                )
            ),
        )
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

    return "test"


if __name__ == '__main__':
    app.run_server(debug=True)
