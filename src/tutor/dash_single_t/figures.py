import sqlite3
from importlib import resources

import dash
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash import html


def get_database_connection():
    """
    Create a connection to the SQLite database.

    Returns:
    conn: sqlite3.Connection object
    """
    path_db = resources.files("tutor.data").joinpath("paralympics.db")
    conn = sqlite3.connect(str(path_db))
    with conn:
        conn.execute("PRAGMA foreign_keys = ON")
        # conn.set_trace_callback(print)
        return conn


def create_line_chart(feature):
    """ Creates a line chart with data from paralympics_events.csv

    Data is displayed over time from 1960 onwards.
    The figure shows separate trends for the winter and summer events.

     Parameters
     feature: events, sports, participants or countriews

     Returns
     fig: Plotly Express line figure
     """

    # take the feature parameter from the function and check it is valid
    if feature not in ["sports", "participants", "events", "countries"]:
        raise ValueError(
            'Invalid value for "feature". Must be one of ["sports", "participants", "events", "countries"]')
    else:
        # Make sure it is lowercase to match the dataframe column names
        feature = feature.lower()

    # Read the data from .csv into a DataFrame
    cols = ["type", "year", "host", feature]
    csv_path = resources.files("tutor.data").joinpath("paralympics.csv")
    line_chart_data = pd.read_csv(str(csv_path), usecols=cols)

    # Create a Plotly Express line chart with the following parameters
    #  line_chart_data is the DataFrame
    #  x="year" is the column to use as the x-axis
    #  y=feature is the column to use as the y-axis
    # color="type" indicates if winter or summer
    feature_txt = feature.capitalize()
    fig = px.line(line_chart_data, x="year", y=feature, color="type",
                  title=f"How has the number of {feature} changed over time?",
                  template="simple_white",
                  labels={
                      "year": "Year",
                      "type": "",
                      "ylabel": feature_txt},
                  )
    return fig


def create_bar_chart(event_type):
    """
    Creates a stacked bar chart showing change in the ratio of male and female competitors in the summer and winter paralympics.

    Parameters
    event_type: str Winter or Summer

    Returns
    fig: Plotly Express bar chart
    """
    cols = ['type', 'year', 'host', 'participants_m', 'participants_f', 'participants']
    csv_path = resources.files("tutor.data").joinpath("paralympics.csv")
    df_events = pd.read_csv(str(csv_path), usecols=cols)
    # Drop Rome as there is no male/female data
    # Drop rows where male/female data is missing
    df_events = df_events.dropna(subset=['participants_m', 'participants_f'])
    df_events.reset_index(drop=True, inplace=True)

    # Add new columns that each contain the result of calculating the % of male and female participants
    df_events['Male'] = df_events['participants_m'] / df_events['participants']
    df_events['Female'] = df_events['participants_f'] / df_events['participants']

    # Sort the values by Type and Year
    df_events.sort_values(['type', 'year'], ascending=(True, True), inplace=True)
    # Create a new column that combines Location and Year to use as the x-axis
    df_events['xlabel'] = df_events['host'] + ' ' + df_events['year'].astype(str)

    # Create the stacked bar plot of the % for male and female
    df_events = df_events.loc[df_events['type'] == event_type]
    fig = px.bar(df_events,
                 x='xlabel',
                 y=['Male', 'Female'],
                 title=f'How has the ratio of female:male participants changed in {event_type} paralympics?',
                 labels={'xlabel': '', 'value': '', 'variable': ''},
                 template="simple_white"
                 )
    fig.update_xaxes(ticklen=0)
    fig.update_yaxes(tickformat=".0%")
    return fig


def create_scatter_geo():
    # create database connection using the get_database_connection function in this file
    connection = get_database_connection()

    # define the sql query
    sql = '''
        SELECT event.year, host.host, host.latitude, host.longitude FROM event
        JOIN host_event ON event.event_id = host_event.event_id
        JOIN host on host_event.host_id = host.host_id
        '''

    df_locs = pd.read_sql(sql=sql, con=connection, index_col=None)
    # The lat and lon are stored as string but need to be floats for the scatter_geo
    df_locs['longitude'] = df_locs['longitude'].astype(float)
    df_locs['latitude'] = df_locs['latitude'].astype(float)
    # Adds a new column that concatenates the city and year e.g. Barcelona 2012
    df_locs['name'] = df_locs['host'] + ' ' + df_locs['year'].astype(str)

    fig = px.scatter_geo(df_locs,
                         lat=df_locs.latitude,
                         lon=df_locs.longitude,
                         hover_name=df_locs.name,
                         title="Where have the paralympics been held?",
                         )
    return fig


def create_card(host_year):
    """
    Generate a card for the event specified by host city name and year.

    Parameters:
        host_year: str  String with the host city name followed by a space then the year.

    Returns:
        card: dash boostrap components card for the event
    """
    # Access substrings to get the year and host as separate values.
    # The last 4 digits are the year, the 5th from last is a space, and the rest is the host
    year = host_year[-4:]
    host = host_year[:-5]

    # Read the data into a DataFrame using a database query
    conn = get_database_connection()
    with conn:
        query = "SELECT * FROM event JOIN  host_event ON event.event_id = host_event.event_id JOIN host ON host_event.host_id = host.host_id WHERE event.year = ? AND host.host = ?;"
        ev = pd.read_sql_query(query, conn, params=[year, host])
        if ev.empty:
            return dbc.Alert("Event not found", color="danger")

        # Variables for the card contents
        logo = f'logos/{year}_{host}.jpg'
        participants = f'{ev['participants'].item()} athletes'
        events = f'{ev['events'].item()} events'
        countries = f'{ev['countries'].item()} participating teams'
        sports = f'{ev['sports'].item()} sports'

        card = dbc.Card([
            dbc.CardImg(src=dash.get_asset_url(logo), style={'max-width': '60px'}, top=True),
            dbc.CardBody([
                html.H4(host_year, className="card-title", id='card-title'),
                html.P(participants, className="card-text", ),
                html.P(events, className="card-text", ),
                html.P(countries, className="card-text", ),
                html.P(sports, className="card-text", ),
            ]),
        ],
            style={"width": "18rem"},
        )
        return card
