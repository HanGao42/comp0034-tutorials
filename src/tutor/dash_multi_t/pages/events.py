# Page with the map and stats card
import dash
import dash_bootstrap_components as dbc
from dash import html

# register the page in the app, this is the default page
dash.register_page(__name__, name='Events', title='Events', path="/", )

# layout defined as a variable named 'layout'. This is the variable name that is specified in the Dash documentation.
layout = dbc.Container([
    dbc.Row([
        dbc.Col([
            html.H1("Event Details", id="event-h1"),
            html.P(
                "Event details. Select a marker on the map to display the event highlights and summary data.")
        ], width=12),
    ]),
    dbc.Row([
        dbc.Col(children=[
            html.Img(src=dash.get_asset_url("map-placeholder.png"), id="map", className="img-fluid"),
        ], width=8),
        dbc.Col(children=[
            dbc.Card([
                dbc.CardImg(src=dash.get_asset_url("logos/2022_Beijing.jpg"), top=True),
                dbc.CardBody([
                    html.H4("Beijing 2022", className="card-title"),
                    html.P("Highlights of the paralympic event will go here. This will be a sentence or two.",
                           className="card-text", ),
                    html.P("Number of athletes: XX", className="card-text", ),
                    html.P("Number of events: XX", className="card-text", ),
                    html.P("Number of countries: XX", className="card-text", ),
                ]),
            ],
                style={"width": "18rem"},
            )], width=4),
    ], align="start")
])
