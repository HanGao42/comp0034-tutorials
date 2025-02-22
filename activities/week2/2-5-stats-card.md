# 4. Card

Summary statistics presented in a Bootstrap card. This is not a chart so does not use Plotly Express or Go.

This example accesses the data from a DataFrame.

The following sources may be useful:

- [dash-bootstrap-components card](https://dash-bootstrap-components.opensource.faculty.ai/docs/components/card/)
- [Charming Data video](https://www.youtube.com/watch?v=THB9AEwdSXo) on advanced aspects of the `dbc.Card` component.

The card will display the details for a selected event.

Next week you will add a callback that changes the event card based on clicks on the map markers.

## Code to create the chart

The Card code currently looks like this:

```python
dbc.Card([
    dbc.CardImg(src=dash.get_asset_url("logos/2022_Beijing.jpg"), top=True),
    dbc.CardBody([
        html.H4("Beijing 2022", className="card-title"),
        html.P("Number of athletes: XX", className="card-text", ),
        html.P("Number of events: XX", className="card-text", ),
        html.P("Number of countries: XX", className="card-text", ),
    ]),
],
    style={"width": "18rem"},
)
```

Modify the existing Card code so that it is a function:

- The function takes a string in the format 'host year' as a parameter. This scatter geo currently uses this for each
  map marker.
- In the function, split the string 'host year' on the space and use the values to find the corresponding row in the
  DataFrame.
- Replace the text in the `H4` and `P` components with variable names that are relevant values from the row.

If you are not sure how to write the function yourself, the following is a possible code structure for the function with comments to guide you as to what to add. 

```python
from importlib import resources
import sqlite3

import pandas as pd
import dash
from dash import html
import dash_bootstrap_components as dbc


def create_card(host_year):
    """
    Generate a card for the event specified by host city name and year.

    Parameters:
        host_year: str  String with the host city name followed by a space then the year

    Returns:
        card: dash boostrap components card for the event
    """
    # Slice the string to get the year and host as separate values.
    # See https://www.w3schools.com/python/python_strings_slicing.asp
    # The last 4 digits are the year
    year = host_year[]# add code in the brackets to get a slice of the string
    # Drop the last 5 digits (a space followed by the year) to the host city 
    host = host_year[]# add code in the brackets to get a slice of the string
    
    # Read the data into a DataFrame from the SQLite database
    with resources.path("data", "paralympics.db") as path:
        conn = sqlite3.connect(path)
        with conn:
            conn.execute("PRAGMA foreign_keys = ON")
            query = "SELECT * FROM event JOIN  host_event ON event.event_id = host_event.event_id JOIN host ON host_event.host_id = host.host_id WHERE event.year = ? AND host.host = ?;"
            event_df = pd.read_sql_query(query, conn, params=[year, host])
    
            # Variables for the card contents, the first is done for you as an example
            logo_path = f'logos/{year}_{host}.jpg'
            highlights = 
            participants = 
            events = 
            countries = 
    
            card = dbc.Card([
                dbc.CardImg(src=dash.get_asset_url(logo_path), style={'max-width': '60px'}, top=True),
                dbc.CardBody([
                    html.H4(host_year, 
                            className="card-title"),
                    html.P(highlights, className="card-text", ),
                    html.P(participants, className="card-text", ),
                    html.P(events, className="card-text", ),
                    html.P(countries, className="card-text", ),
                ]),
            ],
                style={"width": "18rem"},
            )
            return card
```

## Create the card and add it to the layout

Create an instance of the card e.g. `card = create_card("Barcelona 1992")`

Add the card into the layout e.g. `dbc.Col(children=[card], id='card', width=4),`

Check in the running app that the card is displayed.

[Next activity](2-6-challenge.md)