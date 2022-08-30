import dash
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc, html
from dash.dependencies import Input, Output, State


# Constants
title = "Climate Change Tweets - EDA"


# Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = title


# Reading the data file.
# added encoding because data also has emojis
tweets = pd.read_csv('./data/climate_change_tweets_v2.csv', encoding="utf-8")

# Constant Figures
# Monthly Tweets
monthly_stats = tweets.groupby(["month_name", "month"], as_index=False)["tweet_url"].count().sort_values(by="month").rename(columns={
    "tweet_url": "total_tweets"
})
monthly_stats_fig = px.bar(
    monthly_stats,
    x='month_name',
    y='total_tweets',
    labels={
        "month_name": "Month",
        "total_tweets": "Total Tweets"
    }
)


# Hourly tweets, their impacts thru last 6 months.
hourly_tweets_last_six_months = px.scatter(tweets.sort_values(by=["time"]),
                                           x="date",
                                           y="time",
                                           size="normalized_impact",
                                           hover_name="user_name",
                                           size_max=50,
                                           labels={
    "date": "Date",
    "time": "Time"
}
)

# Set Layout
app.layout = html.Div(children=[
    html.H1('Exploratory Data Analysis - Climate Change Tweets'),
    html.Br(),
    html.H2('Climate Change Tweets - Monthly Trends'),
    dcc.Graph(figure=monthly_stats_fig),
    html.H2('Climate Change Tweets - Hourly Trends with Impacts'),
    dcc.Graph(figure=hourly_tweets_last_six_months)

], className="twelve columns")

# Deploy App
if __name__ == '__main__':
    app.run_server(debug=True)
