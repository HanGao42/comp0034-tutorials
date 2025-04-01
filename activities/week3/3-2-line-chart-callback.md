# Implement the line chart dropdown callback

## Check the Dash app runs

Before making changes, make sure you have a Dash app that runs, e.g.

1. Go to `src/student/dash_single/paralympics_dash.py` and run the app.
2. Go to the URL that is shown in the terminal. By default, this is <http://127.0.0.1:8050>.

If you did not complete the activities in weeks 1 and 2, then you may need to copy and adapt the tutor solution code
from `src/tutor/dash_single_t` including the Python file containing the charts code (e.g. `figures.py`) as well as the
latest `paralympics_dash` app code (there are multiple versions of this for different weeks of the activities).

## Line chart callback

This callback will run when an option is selected in the dropdown selector. It will update the line chart with the
selected type of data. The options in the dropdown are: events, sports, countries and participants.

Add code for the callback after the app layout section in the code.

The basic steps for the callback function are:

1. Define the input(s). This is the component that triggers the change you want to make, i.e. the dropdown selection.
2. Define the output(s). This is the component that should be updated when the input changes, in this case the line
   chart.
3. Write the callback function using the `@callback` decorator. This is the function that will take the input value and
   create an updated line chart based on that value.

### Define the Input

The input is the dropdown selector. Find this in your code. It may look like this:

```python
dbc.Select(
    id="dropdown-category",
    options=[
        {"label": "Events", "value": "events"},
        {"label": "Sports", "value": "sports"},
        {"label": "Countries", "value": "countries"},
        {"label": "Athletes", "value": "participants"},
    ],
    value="events"
)
```

For an `Input` you need to identify:

- the component's id. This lets you find the component on the web page.
- the property of the component that has with the value that you want to use in your callback.

In the above code, the `id` is `id="dropdown-category"`.

The property that you want is the value of the selected option. This is the parameter `value=`.

The Input based on the code above would like this: `Input(component_id='dropdown-category', component_property='value')`

### Output

For an `Outut` you need to identify:

- the component's id. This lets you find the component on the web page.
- the property of the component you want to be updated by the callback function.

The output component is the line chart. For example, `dcc.Graph(id="line-chart", figure=fig_line`.

The `id` in the example above is `line-chart`.

The property of this component that you want to update is the `figure=`.

The output will look like this: `Output(component_id='line-chart', component_property='figure')`

### Callback function

The callback function will create a new line chart by taking the value from the dropdown and pass this to the function
to create the line chart.

The code structure of a callback is like this:

```python
# The callback decorator
@callback(
    # The Output(s)
    Output(component_id='my-output', component_property='children'),
    # The Input(s)
    Input(component_id='my-input', component_property='value')
)
# The function that will make the changes. 
# It takes the value captured from the Input property as the `input_value`. Give this a meaningful name.
# It returns whatever change you want to make in the function. In this example it returns a string with the input value.
def update_output_div(input_value):
    return f'Output: {input_value}'
```

Add code for the callback to update the line chart after the app layout section has been defined.

You may need to change the import to match your package and module names which may be different to what is given in the
example.

The function in the tutor example from last week was called `create_line_chart(feature)` which takes as a parameter a
string to represent the data column (events, sports, countries, athletes) to be displayed in the chart.

The callback will get the 'feature' from the selected dropdown which is your Input and create a line chart of that type.

Give the callback a name that describes what it does. In this case the example is `update_line_chart`.

Putting all the code together, your callback will look something like this:

```python
from dash import Input, Output
from student.dash_single.figures import create_line_chart


# Code omitted here that creates the app and adds the layout

@app.callback(
    Output(component_id='line-chart', component_property='figure'),
    Input(component_id='dropdown-category', component_property='value')
)
def update_line_chart(feature):
    figure = create_line_chart(feature)
    return figure
```

Run the app and use the dropdown to change the data type of the chart. The chart should update.

[Next activity](3-3-bar-chart-callback.md)