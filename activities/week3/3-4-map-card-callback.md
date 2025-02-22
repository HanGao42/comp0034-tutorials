# Implement the callback for the map and card

## Callback behaviour

When you hover over or select a marker in the map that represents a paralymics games, the card should update with data
relevant to that event.

This technique is called cross-filtering and is covered the Dash
tutorial in [Part 3: Interactive Graphing and Crossfiltering](https://dash.plotly.com/interactive-graphing) in the
section 'Update Graphs on Hover'.

### Input

You want to update the card when the map marker point for the event is hovered over

The component id is the id of the map e.g. `dcc.Graph(id='map', figure=map)`

The value you need from of this input is within the `hoverData` property.

The `hoverData` object for the `scatter_geo` points as defined in `figures.py` returns data that looks like this
(I printed the `hoverData` to find the structure as it was not clear from the Plotly documentation):

```python
{'points': [
    {
        'curveNumber': 0,
        'pointNumber': 26,
        'pointIndex': 26,
        'lon': -111.891,
        'lat': 40.7608,
        'location': None,
        'hovertext': 'Salt Lake City 2002',
        'bbox': {
            'x0': 358.1616351292792,
            'x1': 364.1616351292792,
            'y0': 768.858120645785,
            'y1': 774.858120645785
        }
    }
]
}
```

This is a dictionary with list elements within it.

The `hovertext` field is within the `points` list of dictionaries.

To get the value of `hovertext`, you can take as a function input the 'hover_data' from the component, then in the
function, access the value within this like this:`text = hover_data['points'][0]['hovertext']`

### Output

The output is the component that contains the card. In the tutor solution from last week this is a `dbc.Col` component.
Make sure the component you used has an `id`, e.g.

```python
dbc.Col(children=[card], id='card', width=4),
```

The component_property of this component is `children=` will be the stats card layout that is returned from the
`create_card()` function.

### Callback

The callback looks something like this.

The code checks that the values are not None to avoid errors.

```python
from dash import Output, Input
from student.dash_single.figures import create_card


@app.callback(
    Output('card', 'children'),
    Input('map', 'hoverData'),
)
def display_card(hover_data):
    text = hover_data['points'][0]['hovertext']
    if text is not None:
        return create_card(text)
```

[Next activity](3-5-further-info.md)