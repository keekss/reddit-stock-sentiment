# Run with terminal command 'python3 app.py'
# View at http://127.0.0.1:8050/ in your web browser

# Note: you may need to install additional libraries
# if using a virtual environment, e.g.:
## dash
## dash_bootstrap_components
## dash_daq

import pandas as pd
from pandas.core.base import SelectionMixin

import numpy as np

import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table as dt
from dash_table.Format import Format, Scheme, Group
import dash_bootstrap_components as dbc
from plotly.express import data
import dash_daq as daq
from dash.dependencies import Input, Output, State

from dash_bootstrap_templates import load_figure_template

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots



app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SLATE])

app.layout = dbc.Container(fluid = True, children = [
    dbc.Container(fluid = True, children = [
        dbc.Row([
            dbc.Col(
                html.Section([
                    html.H1(
                        'Disney Subreddit Visualizations',
                        id = 'main-title',
                    ),
                    html.H4(
                        'ICS 484 - Final Project, Fall 2021 - Robert Lemon, Clark Whitehead, Kiko Whiteley',
                        style = {'padding-top': '0px'}
                    ),
                ]),
                width = 6
            ),
            dbc.Col(
                html.Section([
                    dbc.Row([
                        dbc.Col([
                            html.H3('Info: Tools &', style = dict(paddingTop = '8px')),
                            html.H3('Libraries Used'),
                            html.Div([
                                dcc.Dropdown(
                                    id = 'extra-info-dropdown',
                                    options =[
                                        dict(label = 'PMAW', value = 'pmaw'),
                                        dict(label = 'Pushshift', value = 'pushshift'),
                                        dict(label = 'yfinance', value = 'yfinance'),
                                    ],
                                ),
                            ])], width = 3),
                        dbc.Col(html.H5(id = 'extra-info-text'), width = 9),
                    ]),
                ])
            )
        ])
    ]),
    dbc.Container(fluid = True, children = [
        dcc.Tabs(
        id = 'tabs',
        colors = {
            'primary': 'black',
            'background': '#393F8F',
            'border': 'whitesmoke'
        },
        parent_className = 'custom-tabs',
        className = 'custom-tabs-container',
        children = [
            dcc.Tab(
                label = '1: Character Mentions',
                value = 'tab-1',
                className = 'graph-tab',
            ),
            dcc.Tab(
                label = '2: Disneyland Ride Sentiments',
                value = 'tab-2',
                className = 'graph-tab',
            ),
            dcc.Tab(
                label = '3: Sentiment & Stock Price vs. Time', 
                value = 'tab-3',
                className = 'graph-tab',
            ),
        ]),
        html.Div(id = 'tabs-content')    
    ]),
])


# Tab 1: Character Mentions

cm_df = pd.read_csv('sampleData/disney_character_count.csv')
# Capitalize names
characters = cm_df['Character'].str.title()

cm_fig = go.Figure(
    go.Bar(x = characters, y = cm_df['Count'])
)

cm_fig.update_layout(
    title = 'Character Mentions among 500,000 r/Disney Comments',
    title_x = 0.5,
    height = 850,
)

tab_1 = dbc.Row([
    dcc.Graph(figure = cm_fig)
])

# Tab 2: Disneyland Ride Sentiments

from sklearn import preprocessing
import folium
import branca
import branca.colormap as cm

df_rides = pd.read_csv("./sampleData/disneyland_rides_lat_long_w_sentiment.csv")

#create a map object
map = folium.Map(location=[33.8121, -117.9190], zoom_start=18)

loc = 'Reddit sentiments shown by ride location, normalized between 0 and 1'
title_html = '''
             <h3 align="center" style="font-size:32px;font-family:Avenir"><b>{}</b></h3>
             '''.format(loc) 
map.get_root().html.add_child(folium.Element(title_html))

#create a feature group
fg = folium.FeatureGroup(name="Disneyland Attractions")

#read in the data
# data = pd.read_csv("disneyland_attractions.csv")
data = df_rides

colormap = cm.LinearColormap(
    colors=['red','green'],
    index=[0,1],vmin=0,vmax=1
)

#iterate through the dataframe and add each attraction to the feature group
for index, row in data.iterrows():
    fg.add_child(folium.Marker(location=[row["lat"], row["long"]], popup="{} : {}".format(row["ride"].upper(), round(row['sentiment'], 2)), icon=folium.Icon(color="black", icon_color=colormap(1-row['sentiment']))))

map.add_child(colormap)
    
#add the feature group to the map
map.add_child(fg)


ride_map = map.save('ride_map.html')

ride_map_frame = html.Iframe(
    id = 'ride_map',
    srcDoc = open('ride_map.html', 'r').read(),
    width = '100%',
    height = '850'
)

tab_2 = dbc.Row([
    ride_map_frame
])

# Tab 3: Reddit Sentiment & Stock Price
# ss => sentiment & stock
ss_price_df = pd.read_csv('sampleData/usable_finance.csv')
ss_prices = ss_price_df['Close_Price']

ss_sentiment_df = pd.read_csv('sampleData/usable_sentiment.csv')
ss_sentiments_raw = ss_sentiment_df['Sentiment']

# Smooth sentiments with a moving average
# Referenced https://stackoverflow.com/questions/14313510/how-to-calculate-rolling-moving-average-using-python-numpy-scipy
def moving_average(x, w):
    return np.convolve(x, np.ones(w), 'valid') / w

ss_sentiments = moving_average(ss_sentiments_raw, 30)

ss_dates = ss_price_df['Date'] # same for both dfs

ss_fig = make_subplots(specs=[[{"secondary_y": True}]])

ss_fig.add_trace(
    go.Scatter(
        x = ss_dates,
        y = ss_prices,
        name = 'Stock Price',
    ),
    secondary_y = False
)

ss_fig.add_trace(
    go.Scatter(
        x = ss_dates,
        y = ss_sentiments,
        name = 'Reddit Sentiment',
    ),
    secondary_y = True
)

ss_fig.update_layout(
    title_text = 'Reddit Sentiment & Stock Price vs. Time'
)


tab_3 = dbc.Row([
    dcc.Graph(figure = ss_fig)
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        return tab_1
    elif tab == 'tab-2':
        return tab_2
    elif tab == 'tab-3':
        return tab_3

extra_info_dict = dict(
    pmaw = 'pmaw info',
    pushshift = '',
    yfinance = 'yfinance info'
)

@app.callback(
   Output('extra-info-text', 'children'),
   Input('extra-info-dropdown', 'value'))
def choose_extra_info(choice):
    if choice and extra_info_dict[choice]:
        return extra_info_dict[choice]
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)
