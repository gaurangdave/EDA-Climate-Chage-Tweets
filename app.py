import dash
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc, html
from dash.dependencies import Input, Output, State


## Constants
title = "Climate Change Tweets - EDA"

# Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = title

## Set Layout
app.layout = html.Div(children=[
     html.H1('Hello World')
])

## Deploy App
if __name__ == '__main__':
     app.run_server(debug=True)