# 1. Line chart

In this activity you will create a line chart using Plotly Express. The data will be read into a pandas DataFrame from a .csv
file.

## Create the chart

Add a [Plotly Express line chart](https://plotly.com/python-api-reference/generated/plotly.express.line.html) that
displays for each paralympics the total number of events, competitors and sports. The data will be displayed over time,
i.e. from 1960 through to 2022.

The data is in `data/paralympics.csv`. The columns needed
are: `["type", "year", "host", "events", "sports", "participants", "countries"]`.

You do not have to put the chart code in a function but doing so can make it easier when you later add callbacks (next
week).

Create a function to create the line chart. The function should take a parameter that accepts whether the chart should display events,
sports or participants.

The following code is commented to explain what it does:

```python
from importlib import resources

import pandas as pd
import plotly.express as px


def line_chart(feature):
    """ Creates a line chart with data from paralympics.csv

    Data is displayed over time from 1960 onwards.
    The figure shows separate trends for the winter and summer events.

     Parameters
     feature: events, sports or participants

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
    # Uses importlib.resources rather than pathlib.Path
    with resources.path("data", "paralympics.csv") as path:
        line_chart_data = pd.read_csv(path, usecols=cols)

        # Create a Plotly Express line chart with the following parameters
        #    line_chart_data is the DataFrame
        #    x="year" is the column to use as the x-axis
        #    y=feature is the column to use as the y-axis
        #    color="type" indicates if winter or summer
        fig = px.line(line_chart_data, x="year", y=feature, color="type")
        return fig
```

Note that if `importlib.resources` does not work for you, you can use pathlib instead e.g.

```python
import pathlib

# path to paralympic data
path = pathlib.Path(__file__).parent.parent.joinpath("data", "paralympics.csv")
```

You can either add the code to the main dash app file, or create a new python file with the code to create chart with a
relevant name such as `charts.py` or `figures.py`.

Adding the code to a separate module keeps the code to generate the charts in one place, and avoids the main app module
becoming too long which can make it harder to read.

## Add the chart to the Dash layout

To do this:

1. Create a variable that is the chart using the function you created in the last step
2. Add a [Dash Core Components graph object](https://dash.plotly.com/dash-core-components/graph), `dcc.Graph()` to the
   layout. This component has a `figure=` attribute. This is the chart (or figure) you just created in step 1. It also
   takes and `id=` which you should set as you will need it in next week's activities, e.g. `id="line-chart"`.

In the Dash main app file, `paralympics_dash.py`, add code to create the chart and then add the chart into the layout.

It might look something like this:

```python
# Add dcc import to imports section
from dash import Dash, html, dcc
# Add an import to import the line_chart function
from dash_single.figures import line_chart

# Create the Plotly Express line chart object, e.g. to show number of sports
line_fig = line_chart("sports")

# Code omitted here for brevity: create the Dash app

app.layout = dbc.Container([
    # Other layout code omitted for brevity

    # Add the chart to the layout
    dcc.Graph(id="line-chart", figure=line_fig)
])
```

If the app is running and your code did not fail, then it should now display the chart you created. If the app is not
running, then run it.

## Style the chart

Refer to the [documentation for styling Express](https://plotly.com/python/styling-plotly-express/) for this activity.

Amend the code that creates the line chart to:

1. Set the figure title to "How has the number of {feature} changed over time?":
   `title=f"How has the number of {feature} changed over time?"`
2. Change the axis labels to remove the word 'feature' from the Y axis and change the X axis label
   to start with a capital letter: e.g.
   ```python
   labels = { 
                 "feature": "",
                 "year": "Year"
             }
   ```
3. Use a template to apply a more simple style that has no background, e.g., `template="simple_white"`

Check the app is running, it should now display the line chart with the revised styling.

[Next activity](2-3-bar-chart.md)