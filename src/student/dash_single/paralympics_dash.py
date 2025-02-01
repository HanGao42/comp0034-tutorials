from dash import Dash, html, dcc
import pathlib
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Variable that defines the meta tag for the viewport
meta_tags = [
    {"name": "viewport", "content": "width=device-width, initial-scale=1"},
]

# Variable that contains the external_stylesheet to use, in this case Bootstrap styling from dash bootstrap components (dbc)
external_stylesheets = [dbc.themes.BOOTSTRAP]

# Pass the stylesheet and meta_tag variables to the Dash app constructor
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Wrap the layout in a Bootstrap container
div_one = html.Div(
    [
        dbc.Row([
            dbc.Col(['Divivion 1']),
        ])
    ],
    className="border border-dark rounded p-4 mb-4"
)

div_two = html.Div(
    [
        dbc.Row([
            dbc.Col(['Col 1'], className="border border-dark rounded p-4 mb-4"),
            dbc.Col(['Col 2'], className="border border-dark rounded p-4 mb-4"),
            dbc.Col(['Col 3'], className="border border-dark rounded p-4 mb-4"),
        ])
    ],
    className="border border-dark rounded p-4 mb-4"
)

div_three = html.Div(
    [
        dbc.Row([
            dbc.Col(['S 4 O 5'], width={"size": 4, "offset": 5}),
        ])
    ],
    className="border border-dark rounded p-4 mb-4"
)

# row_one = dbc.Row(
#     [
#         dbc.Col(
#             html.Div([
#                 html.H1("Paralympics Data Analytics"),
#                 html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent congue luctus elit nec gravida.")
#             ])
#         )
#     ],
#     className="border border-dark rounded p-4 mb-4"
# )

row_one = dbc.Row(
    [
        dbc.Col(
            children=[
                html.H1("Paralympics Data Analytics"),
                html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent congue luctus elit nec gravida.")
            ], width=12,
        )
    ], #className="border border-dark rounded p-4 mb-4"
)

row_two = dbc.Row(
    [
        dbc.Col(
            children=[
                dbc.Select(
                    options=[
                        {"label": "Events", "value": "events"},  # The value is in the format of the column heading in the data
                        {"label": "Sports", "value": "sports"},
                        {"label": "Countries", "value": "countries"},
                        {"label": "Athletes", "value": "participants"},
                    ],
                    value="events",  # The default selection
                    id="dropdown-input",  # id uniquely identifies the element, will be needed later for callbacks
                ),
            ], width=4, #className="border border-dark rounded p-4 mb-4"
        ),

        dbc.Col(
            children=[
                html.Div(
                    [
                        dbc.Label("Select the Paralympic Games type"),
                        dbc.Checklist(
                            options=[
                                {"label": "Summer", "value": "summer"},
                                {"label": "Winter", "value": "winter"},
                            ],
                            value=["summer"],  # Values is a list as you can select 1 AND 2
                            id="checklist-input",
                        ),
                    ]
                )
            ], width={"size": 4, "offset": 2}, #className="border border-dark rounded p-4 mb-4"
        )
    ]
)

row_three = dbc.Row(
    [
        dbc.Col(
            children=[
                html.Img(src=app.get_asset_url('line-chart-placeholder.png'), className="img-fluid")
            ], width=6, #className="border border-dark rounded p-4 mb-4"
        ),

        dbc.Col(
            children=[
                html.Img(src=app.get_asset_url('bar-chart-placeholder.png'), className="img-fluid")
            ], width=6, #className="border border-dark rounded p-4 mb-4"
        )
    ]
)

row_four = dbc.Row(
    [
        dbc.Col(
            children=[
                html.Img(src=app.get_asset_url('map-placeholder.png'), className="img-fluid")
            ], width=8, #className="border border-dark rounded p-4 mb-4"
        ),

        dbc.Col(
            children=[
                dbc.Card(
                    [
                        dbc.CardImg(src=app.get_asset_url("logos/2022_Beijing.jpg"), top=True),
                        dbc.CardBody(
                            [
                                html.H4("Beijing 2022", className="card-title"),
                                html.P("Number of athletes: XX", className="card-text", ),
                                html.P("Number of events: XX", className="card-text", ),
                                html.P("Number of countries: XX", className="card-text", ),
                                html.P("Number of sports: XX", className="card-text", ),
                            ]
                        )
                    ], style={"width": "18rem"},
                ), 
            ], width=4, #className="border border-dark rounded p-4 mb-4"
        )
    ]
)


def line_chart(feature):
    """ Creates a line chart with data from paralympics.csv

    Data is displayed over time from 1960 onwards.
    The figure shows separate trends for the winter and summer events.

     Parameters
     feature: events, sports or participants

     Returns
     fig: Plotly Express line figure
     """

    # Validate feature parameter
    if feature not in ["sports", "participants", "events", "countries"]:
        raise ValueError(
            'Invalid value for "feature". Must be one of ["sports", "participants", "events", "countries"]')
    else:
        feature = feature.lower()

    # Read the data from .csv into a DataFrame
    cols = ["type", "year", "host", feature]
    path = pathlib.Path(__file__).parent.parent.joinpath("data", "paralympics.csv")
    line_chart_data = pd.read_csv(path, usecols=cols)

    # Create the line chart with updated styling requirements
    fig = px.line(
        line_chart_data,
        x="year",
        y=feature,
        color="type",
        labels={
            "year": "Year",   # Capitalize X-axis
            feature: ""       # Remove Y-axis label feature name
        },
        template="simple_white"  # Apply template style
    )

    # Set the figure title dynamically
    fig.update_layout(
        title=f"How has the number of {feature} changed over time?"
    )

    return fig

def bar_gender(event_type):
    """
    Creates a stacked bar chart showing change in the ration of male and female competitors in the summer and winter paralympics.

    Parameters
    event_type: str Winter or Summer

    Returns
    fig: Plotly Express bar chart
    """
    cols = ['type', 'year', 'host', 'participants_m', 'participants_f', 'participants']

    path = pathlib.Path(__file__).parent.parent.joinpath("data", "paralympics.csv")
    df_events = pd.read_csv(path, usecols=cols)
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


line_fig = line_chart("sports")
bar_fig = bar_gender("summer")


app.layout = dbc.Container([
    row_one,
    row_two,
    row_three,
    row_four,
    dcc.Graph(id="line-chart", figure=line_fig),
    dcc.Graph(id="bar-chart", figure=bar_fig)

])


# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5050)