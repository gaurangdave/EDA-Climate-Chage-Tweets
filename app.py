import dash
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from dash import dcc, html
from dash.dependencies import Input, Output, State


# Constants
title = "Climate Change Tweets - EDA"
color_discrete_map={
     "January": px.colors.qualitative.Dark24[0],
     "February": px.colors.qualitative.Dark24[1],
     "March": px.colors.qualitative.Dark24[2],
     "April": px.colors.qualitative.Dark24[3],
     "May": px.colors.qualitative.Dark24[4],
     "June": px.colors.qualitative.Dark24[5],
     "July": px.colors.qualitative.Dark24[6],
     "August":px.colors.qualitative.Dark24[7],
     "September":px.colors.qualitative.Dark24[8],
     "October": px.colors.qualitative.Dark24[9],
     "November": px.colors.qualitative.Dark24[10],
     "December":px.colors.qualitative.Dark24[11] 
}

# Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
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
    }
)

## Monthly Trends Breakdown
monthly_trends_breakdown = tweets.groupby(["month","month_name", "day"], as_index=False)["text"].count()
monthly_trends_breakdown_fig = px.line(monthly_trends_breakdown, x="day", y="text", color='month_name', color_discrete_map=color_discrete_map,labels={
     "month_name": "Month",
     "day": "Date",
     "text": "Number of Tweets"
})
monthly_trends_breakdown_fig.update_xaxes(dtick=1)



# Tweet Impact Trends
tweet_impact_trends = px.scatter(
    tweets.loc[:, ["timestamp", "normalized_impact"]],
    x="timestamp",
    y="normalized_impact",
    labels={
        "normalized_impact": "Normalized Impact",
        "timestamp": "Time"
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
    dcc.Graph(figure=monthly_trends_fig),
    html.H2('Climate Change Tweets - Monthly Trends Breakdown'),
    dcc.Graph(figure=monthly_trends_breakdown_fig),
    html.H2('Climate Change Tweets - Hourly Trends with Impact'),
    dcc.Graph(figure=hourly_tweets_last_six_months),
    html.H2('Climate Change Tweets - Tweet Impact Trends'),
    dcc.Graph(figure=tweet_impact_trends)

], className="twelve columns")

# Deploy App
if __name__ == '__main__':
    app.run_server(debug=True)
