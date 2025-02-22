""" App code as at the end of week 1 activities"""
import dash_bootstrap_components as dbc
from dash import Dash, html


meta_tags = [{"name": "viewport", "content": "width=device-width, initial-scale=1"}, ]
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Variables that define each row that will be added to the layout
row_one = dbc.Row([
    dbc.Col([
        html.H1("Paralympics Dashboard", id='title'),
        html.P("Try to answer the questions using the charts below.")
    ], width=12),
])

row_two = dbc.Row([
    dbc.Col(children=[
        dbc.Select(
            id="dropdown-category",
            options=[
                {"label": "Events", "value": "events"},
                {"label": "Sports", "value": "sports"},
                {"label": "Countries", "value": "countries"},
                {"label": "Athletes", "value": "participants"},
            ],
            value="events"
        )], width=4),
    dbc.Col(children=[
        dbc.Checklist(
            options=[
                {"label": "Summer", "value": "summer"},
                {"label": "Winter", "value": "winter"},
            ],
            value=["summer"],
            id="checklist-games-type",
        )
    ], width={"size": 4, "offset": 2}),
])

row_three = dbc.Row([
    dbc.Col(children=[
        # Add the dcc.Graph() for the line chart and delete the image
        html.Img(src=app.get_asset_url('line-chart-placeholder.png'), className="img-fluid", alt="Line chart",id='line-chart'),
    ], width=6),
    dbc.Col(children=[
        # Add the dcc.Graph() for the line chart and delete the image
        html.Img(src=app.get_asset_url('bar-chart-placeholder.png'),id='bar-chart', className="img-fluid", alt="Bar chart"),
    ], width=6),
], align="start")

row_four = dbc.Row([
    dbc.Col(children=[
        html.Img(src=app.get_asset_url('map-placeholder.png'), id='map', className="img-fluid", alt="Map"),
    ], width=8),
    dbc.Col(children=[
        # The card will go here
    ], id='card', width=4),
], align="start")

app.layout = dbc.Container([
    row_one,
    row_two,
    row_three,
    row_four
])

if __name__ == '__main__':
    app.run(debug=True)
