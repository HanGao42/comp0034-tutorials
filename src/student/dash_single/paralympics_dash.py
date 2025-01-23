from dash import Dash, html
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

app.layout = dbc.Container([
    html.H1("Paralympics Data Analytics", className="border border-dark rounded p-4 mb-4"),
    html.P("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent congue luctus elit nec gravida.", className="border border-dark rounded p-4 mb-4"),
    div_one,
    div_two,
    div_three
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True, port=5050)