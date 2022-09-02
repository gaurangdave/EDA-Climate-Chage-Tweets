import dash
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


# Constants
title = "Climate Change Tweets - EDA"
color_discrete_map = {
    "January": px.colors.qualitative.Dark24[0],
    "February": px.colors.qualitative.Dark24[1],
    "March": px.colors.qualitative.Dark24[2],
    "April": px.colors.qualitative.Dark24[3],
    "May": px.colors.qualitative.Dark24[4],
    "June": px.colors.qualitative.Dark24[5],
    "July": px.colors.qualitative.Dark24[6],
    "August": px.colors.qualitative.Dark24[7],
    "September": px.colors.qualitative.Dark24[8],
    "October": px.colors.qualitative.Dark24[9],
    "November": px.colors.qualitative.Dark24[10],
    "December": px.colors.qualitative.Dark24[11]
}

# Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
app.title = title


# Reading the data file.
# added encoding because data also has emojis
tweets = pd.read_csv('./data/climate_change_tweets_v2.csv', encoding="utf-8")

# Constant Figures
# Monthly Trends
monthly_trends = tweets.groupby(["month_name", "month"], as_index=False)["tweet_url"].count().sort_values(by="month").rename(columns={
    "tweet_url": "total_tweets"
})
monthly_trends_fig = px.bar(
    monthly_trends,
    x='month_name',
    y='total_tweets',
    color_discrete_map=color_discrete_map,
    labels={
        "month_name": "Month",
        "total_tweets": "Total Tweets"
    },
    title="Number of Climate Change Tweets each month."
)

# Monthly Trends Breakdown
monthly_trends_breakdown = tweets.groupby(
    ["month", "month_name", "day"], as_index=False)["text"].count()

monthly_trends_breakdown_fig = px.line(monthly_trends_breakdown, x="day", y="text", color='month_name', color_discrete_map=color_discrete_map, labels={
    "month_name": "Month",
    "day": "Date",
    "text": "Number of Tweets"
},
    title="Daily breakdown of monthly trends"
)
monthly_trends_breakdown_fig.update_xaxes(dtick=1)


# Tweet Impact Trends
tweet_impact_trends = px.scatter(
    tweets.loc[:, ["timestamp", "normalized_impact"]],
    x="timestamp",
    y="normalized_impact",
    labels={
        "normalized_impact": "Normalized Impact",
        "timestamp": "Time"
    },
    title="Distribution of tweets and their impacts."
)


# Hourly tweets, their impacts thru last 6 months.
hourly_tweets_last_six_months = px.scatter(tweets.sort_values(by=["time"]),
                                           x="date",
                                           y="time",
                                           size="normalized_impact",
                                           hover_name="user_name",
                                           color_discrete_map=color_discrete_map,
                                           size_max=50,
                                           labels={
    "date": "Date",
    "time": "Time"
},
    title="Hourly Breakdown - Size of the point represents the impact (retweets + likes + number of comments) of the tweet."
)

# Types of Tweets
hashtag_condition = tweets["hashtag_count"] > 0

# Number of tweets with hashtags vs number of tweets without hashtags.
type_of_tweet_data = {
    "Type": ["Tweets with atleast one hashtag", "Tweets without any hashtags"],
    "Count": [tweets[hashtag_condition]["text"].count(), tweets[~hashtag_condition]["text"].count()]
}

type_of_tweet_fig = px.pie(pd.DataFrame(
    type_of_tweet_data), values='Count', names='Type', title="Distribution of tweets with hashtags vs tweets without hashtags.")

# Set Layout
app.layout = html.Div(children=[
    dbc.Row(html.H1('Exploratory Data Analysis - Climate Change Tweets',
            style={'textAlign': 'center'})),
    html.Br(),
    dbc.Row(html.H3('Monthly Trends',
            style={'textAlign': 'center'})),
    dbc.Row(
        [
            dbc.Col(
                html.Div(children=[
                    html.H4('Observations'),
                    html.Ul(children=[
                        html.Li("Total Number of Tweets : 9050"),
                        html.Li("Average Monthly Tweets : ~1293"),
                        html.Li("Max Monthly Tweets : 1678 (First half of July)"),
                        html.Li(
                            "Min Monthly Tweets : 641 (Second half of January)"),
                    ])
                ]),
                width=3
            ),
            dbc.Col(dcc.Graph(figure=monthly_trends_fig), width=9)
        ]
    ),
    dbc.Row(html.H3('Monthly Trends Breakdown',
            style={'textAlign': 'center'})),
    dbc.Row(
        [
            dbc.Col(
                html.Div(children=[
                    html.H4('Observations'),
                    html.Ul(children=[
                        html.Li("Average Daily Tweets : 49"),
                        html.Li("Max Tweets in a day : 175 (07/12/2022)"),
                        html.Li("Min Tweets in a day : 29 (06/01/2022)"),
                        html.Li(
                            "Spike on 07/11 and 07/12 could be mostly likely due US Supreme Court ruling related to EPA"),
                    ])
                ]),
                width=3
            ),
            dbc.Col(dcc.Graph(figure=monthly_trends_breakdown_fig), width=9)
        ]
    ),
    dbc.Row(html.H3('Hourly Trends with Impact',
            style={'textAlign': 'center'})),
    dbc.Row([
        dbc.Col(
            html.Div(children=[
                html.H4('Observations'),
                html.Ul(
                    children=[
                     html.Li("Average Impact : 0.00222"),
                     html.Li("Maximum Impact : 1.0"),
                     html.Li("Minimum Impact : 0.0"),
                     html.Li(
                         "Normally people tweet about climate change between 6:30 PM to 11:30 PM."),
                     html.Li(
                         "Except for the month of July when climate change was a trending topic and users discussed it on twitter through out the day. "),
                     ])
            ]),
            width=3
        ),
        dbc.Col(dcc.Graph(figure=hourly_tweets_last_six_months), width=9)
    ]),
    dbc.Row(html.H3('Tweet Impact Trends',
            style={'textAlign': 'center'})),
    dbc.Row([
        dbc.Col(
            html.Div(children=[
                html.H4('Observations'),
                  html.Ul(
                    children=[
                     html.Li("Average Impact : 0.00222"),
                     html.Li("Maximum Impact : 1.0"),
                     html.Li("Minimum Impact : 0.0"),
                     html.Li(
                         "Majority tweets have impact < 0.4"),
                     html.Li(
                         "Outlier tweet with impact 1 is from POTUS"),
                     ])
    
            ]),
            width=3
        ),
        dbc.Col(dcc.Graph(figure=tweet_impact_trends), width=9)
    ]),
    dbc.Row(html.H3('Tweets with Hashtags vs without Hashtags',
            style={'textAlign': 'center'})),
    dbc.Row([
        dbc.Col(
            html.Div(children=[
                html.H4('Observations'),
                html.Ul(
                    children=[
                        html.Li("Going against common intuition that tweets normally have hashtags - majority climate change tweets do not have hashtags associated with them.")
                    ]
                )
            ]),
            width=3
        ),
        dbc.Col(dcc.Graph(figure=type_of_tweet_fig), width=9)
    ])

], className="twelve columns")

# Deploy App
if __name__ == '__main__':
    app.run_server(debug=True)
