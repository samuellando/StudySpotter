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



data = response.json()
print(data)



#df[" Last time seen"] = pd.to_datetime(df[" Last time seen"], format="%Y-%m-%d %H:%M")
#df.index = df[" Last time seen"]
#df.drop(" Last time seen", 1, inplace=True)

app.layout = html.Div([
    dcc.Graph(
        figure=go.Figure(
            data=[  
                Scattermapbox(
                    lat=[list_of_locations["Trottier"]["lat"]],
                    lon=[list_of_locations["Trottier"]["lon"]],
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
    dcc.Graph(
        figure=go.Figure(
            data=[
                go.Bar(x=[list_of_locations["Trottier"]["lat"]], y=[list_of_locations["Trottier"]["lon"]], marker=dict(color="red"), hoverinfo="x")
            ]
        )
    )
])





if __name__ == '__main__':
    app.run_server(debug=True)
