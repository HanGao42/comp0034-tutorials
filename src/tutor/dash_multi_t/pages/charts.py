# Page with the line chart and bar chart and their selectors
import dash
import dash_bootstrap_components as dbc
from dash import html

# register the page in the app
dash.register_page(__name__, name="Charts", title="Charts")


# This uses the option to create the layout as a function
# see https://dash.plotly.com/urls#layout
def layout(**kwargs):
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1("Charts"),
                html.P("Try to answer the questions using the charts below.")
            ], width=12),
        ]),
        dbc.Row([
            dbc.Col(children=[
                dbc.Select(
                    id="dropdown-category",  # id uniquely identifies the element, will be needed later
                    options=[
                        {"label": "Events", "value": "events"},
                        # The value is in the format of the column heading in the data
                        {"label": "Sports", "value": "sports"},
                        {"label": "Countries", "value": "countries"},
                        {"label": "Athletes", "value": "participants"},
                    ],
                    value="events"  # The default selection
                )], width=4),
            dbc.Col(children=[
                dbc.Checklist(
                    options=[
                        {"label": "Summer", "value": "summer"},
                        {"label": "Winter", "value": "winter"},
                    ],
                    value=["summer"],  # Values is a list as you can select both winter and summer, summer is default
                    id="checklist-games-type",
                )
            ], width={"size": 4, "offset": 2}),
        ]),
        dbc.Row([
            dbc.Col(children=[
                # Placeholder image to represent the chart
                html.Img(src=dash.get_asset_url("line-chart-placeholder.png"), id="line-chart", className="img-fluid"),
            ], width=6),
            dbc.Col(children=[
                # Placeholder image to represent the chart
                html.Img(src=dash.get_asset_url("bar-chart-placeholder.png"), id="bar-chart", className="img-fluid"),
            ], width=6),
        ],
            align="start")
    ])
