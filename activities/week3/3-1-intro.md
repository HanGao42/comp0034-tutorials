# Tutorial 3: Adding interactivity with callbacks

## Introduction

A callback function is a Python function that is automatically called by Dash whenever an input component's property
changes. For example, when a user makes a choice from a dropdown list or ticks a checkbox.

The basic steps for the callback function are:

- Define the input(s)
- Define the output(s)
- Write the callback function using the `@callback` decorator

With a structure like this:

```python
from dash import Input, Output


# Code omitted here that creates the app and adds the layout

# After the app is created you can define the callbacks
@app.callback(
    Output(component_id='my-output', component_property='children'),
    Input(component_id='my-input', component_property='value')
)
def update_output_div(input_value):
    return f'Output: {input_value}'
```

You may need to refer to the [Dash callback documentation](https://dash.plotly.com/basic-callbacks).

## `@callback` decorator rules

- The decorator tells Dash to call the function for us whenever the value of the "input" component (e.g. a text box)
  changes in order to update the children of the "output" component on the page (e.g. an HTML div).
- You can use any name for the function that is wrapped by the @app.callback decorator. The convention is that the name
  describes the callback output(s).
- You can use any name for the function arguments, but you must use the same names inside the callback function as you
  do in its definition, just like in a regular Python function. The arguments are positional: first the Input items and
  then any State items are given in the same order as in the decorator.
- You must use the same id you gave a Dash component in the app.layout when referring to it as either an input or output
  of the @app.callback decorator.
- The @app.callback decorator needs to be directly above the callback function declaration. If there is a blank line
  between the decorator and the function definition, the callback registration will not be successful.

## Callback 'gotchas'

[callback gotchas](https://dash.plotly.com/callback-gotchas):

- Callbacks require their Inputs, States, and Output to be present in the layout
- Callbacks require all Inputs and States to be rendered on the page
- All callbacks must be defined before the server starts
- Callback definitions don't need to be in lists (in earlier versions they were and some tutorials will show this)

## Using `State` for "form"-like input

You may also define `State` in a callback. This is used where there is a "form"-like pattern to the input. That is, you
may want to read
the value of an input component, but only when the user is finished entering all their information in the form rather
than immediately after it changes.

There is no example with State in this tutorial. The following example is from
the [Dash documentation](https://dash.plotly.com/basic-callbacks#dash-app-with-state).

```python
from dash import Dash, dcc, html, Input, Output, callback

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div([
    dcc.Input(id="input-1", type="text", value="Montréal"),
    dcc.Input(id="input-2", type="text", value="Canada"),
    html.Div(id="number-output"),
])


@callback(
    Output("number-output", "children"),
    Input("input-1", "value"),
    Input("input-2", "value"),
)
def update_output(input1, input2):
    return f'Input 1 is "{input1}" and Input 2 is "{input2}"'


if __name__ == "__main__":
    app.run(debug=True)
```

[Next activity](3-2-line-chart-callback.md)