""" Version as at the end of week 3: Charts with callbacks"""
import dash_bootstrap_components as dbc
from dash import Dash, Input, Output, dcc, html

from tutor.dash_single_t.figures import create_bar_chart, create_card, create_line_chart, create_scatter_geo

meta_tags = [{"name": "viewport", "content": "width=device-width, initial-scale=1"}, ]
external_stylesheets = [dbc.themes.BOOTSTRAP]
app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)

# Create the figure (chart) variables
fig_line = create_line_chart("sports")
fig_bar = create_bar_chart("winter")
map = create_scatter_geo()
card = create_card("Sydney 2000")

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
    dbc.Col(children=[dcc.Graph(id="line-chart", figure=fig_line), ], width=6),
    dbc.Col(children=[], id='bar-div', width=6),
], align="start")

row_four = dbc.Row([
    dbc.Col(children=[dcc.Graph(id='map', figure=map)], width=8),
    dbc.Col(children=[card], id='card', width=4),
], align="start")

app.layout = dbc.Container([
    row_one,
    row_two,
    row_three,
    row_four
])


@app.callback(
    Output(component_id='line-chart', component_property='figure'),
    Input(component_id='dropdown-category', component_property='value')
)
def update_line_chart(feature):
    """ Update the line chart based on the dropdown selection """
    figure = create_line_chart(feature)
    return figure


# This version removes the original bar chart component from the layout and treats the Col as the Output
@app.callback(
    Output(component_id='bar-div', component_property='children'),
    Input(component_id='checklist-games-type', component_property='value')
)
def update_bar_chart(selected_values):
    """ Updates the bar chart based on the checklist selection.
     Creates one chart for each of the selected values.
     """
    figures = []
    # Iterate the list of values from the checkbox component
    for value in selected_values:
        fig = create_bar_chart(value)
        # Assign id to be used to identify the charts
        id = f"bar-chart-{value}"
        element = dcc.Graph(figure=fig, id=id)
        figures.append(element)
    return figures


@app.callback(
    Output('card', 'children'),
    Input('map', 'hoverData'),
)
def display_card(hover_data):
    """ Display a card with information about the selected country on the map """
    if hover_data is not None:
        text = hover_data['points'][0]['hovertext']
        return create_card(text)


if __name__ == '__main__':
    app.run(debug=True)
