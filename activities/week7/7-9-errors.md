# Logging and handling errors

In this activity you will:

1. Use the logger to track events while the server is being used (useful for debugging)
2. Configure Flask to return bespoke error pages for '404 Not found' and '500 Internal server error'
3. Recap: using Python try/except to handle errors

## 1. Use logging to track events in a running Flask app

You can use logging to track events that happen when the server is running and the application is being used. This
can make troubleshooting errors easier as helps you see what is going on in your application.

With logging, you can use different functions to report information on different logging levels. Each level indicates an
event happened with a certain degree of severity. The following functions can be used:

- app.logger.debug(): For detailed information about the event.
- app.logger.info(): Confirmation that things are working as expected.
- app.logger.warning(): Indication that something unexpected happened (such as “disk space low”), but the application is
  working as expected.
- app.logger.error(): An error occurred in some part of the application.
- app.logger.critical(): A critical error; the entire application might have stop working.

You can add these to your code. For example, the app logger is used in the exception handling of the try/except
in the route below:

```python
@app.get('/regions/<code>')
def get_region(code):
    try:
        region = db.session.execute(db.select(Region).filter_by(NOC=code)).scalar_one()
        result = region_schema.dump(region)
        return result
    except exc.NoResultFound as e:
        app.logger.error(f'Region code {code} was not found. Error: {e}')
        abort(404, description="Region not found")
```

You can log events for information, for example in the startup in `create_app()`:

```python
import logging


def create_app():
    logging.basicConfig(filename='paralympics-error.log', level=logging.DEBUG)
    app = Flask(__name__)

    # app config, database, and other code omitted here

    app.logger.info(f"The app is starting...")

    return app
```

You would then see the log result in the terminal, e.g.:

```text
[2023-12-31 15:35:56,789] ERROR in routes: Region code ZZA was not found. Error: No row was found when one was required
127.0.0.1 - - [31/Dec/2023 15:35:56] "GET /regions/ZZA HTTP/1.1" 404 -
```

It is likely more useful to output the log records to a file.

To do this, you need to configure Logging before the app starts.

Add the following the `create_app()` function.

This is copied and adapted from
the [Flask documentation](https://flask.palletsprojects.com/en/stable/logging/#logging) with more detail on the
dictConfig parameters in
this [blog post](https://betterstack.com/community/guides/logging/how-to-start-logging-with-flask/):

```python
from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers':
        {'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        },
            "file": {
                "class": "logging.FileHandler",
                "filename": "paralympics_log.log",
                "formatter": "default",
            },
        },
    "root": {"level": "DEBUG", "handlers": ["wsgi", "file"]},
})

# create and configure the app
app = Flask(__name__, instance_relative_config=True)

```

Try running the app and check for the log file `paralympics-error.log`.

## 2. Custom error views in Flask

The Flask documentation
for [handling application errors in Flask](https://flask.palletsprojects.com/en/stable/errorhandling/) explains how to
add custom errors.

You can either decorate a function with `@app.errorhander()` or write a function and then register it using
`app.register_error_handler()`.

The following approach can be used with the Application Factory pattern:

- Define an error handling function. The function returns a custom error template.
- Register the error handler within the `create_app()` function.

### Create a custom 500 error handler

1. Create a template for 500 error

    ```jinja
    {% extends "layout.html" %}
    {% block title %}Server error{% endblock %}
    {% block body %}
        <h1>Oops! Something went wrong at our end.</h1>
        <p><a href="{{ url_for('main.index') }}">go back to the home page</a>
    {% endblock %}
    ```
2. Define the error handler function that overrides the default

   Add the following to `__init__.py` (or elsewhere and import it):

    ```python
    def internal_server_error(e):
      return render_template('500.html'), 500
    ```

3. Register the error handler in the `create_app()` function e.g.
    ```python
    def create_app():
        app = Flask(__name__)
        app.register_error_handler(500, internal_server_error)
        return app
   ```

Try it yourself, add a custom error handler for `404 Not found` errors.

## 3. Use Python try / except in routes

Even if a statement or expression is syntactically correct, it may cause an error when an attempt is made to execute it.
Errors detected during execution are called `exceptions`. Source: Python

The `Try Except` block can include the following elements:

- The `try` block lets you test a block of code for errors.
- The `except` block lets you handle the error.
- The `else` block lets you execute code when there is no error.
- The `finally` block lets you execute code, regardless of the result of the try- and except blocks.

Source: w3schools

```python
def divide(x, y):
    try:
        # Floor Division : Gives only Fractional Part as Answer 
        result = x // y
    except ZeroDivisionError:
        print("Sorry ! You are dividing by zero ")
    else:
        print("Yeah ! Your answer is :", result)
    finally:
        # this block is always executed   
        # regardless of exception generation.  
        print('This is always executed')

        # Source: https://www.geeksforgeeks.org/try-except-else-and-finally-in-python/
```

Consider the following code:

```python
@app.delete('/regions/<noc_code>')
def delete_region(noc_code):
    """ Deletes the region with the given code.

    Args:
        param code (str): The 3-character NOC code of the region to delete
    Returns:
        JSON format message
    """
    region = db.session.execute(db.select(Region).filter_by(NOC=noc_code)).scalar_one()
    db.session.delete(region)
    db.session.commit()
    return {"message": f"Region {noc_code} deleted."}
```

This is OK if the Region code is found in the database, but if a code is passed that is not found in the database then
an error would occur.

A better solution would be to return an error if the Region is not found. There are different ways to achieve this.

1. [Flask-SQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/queries/#queries-for-views) provides some extra
   query methods.

    - `.get_or_404()` will raise a 404 if the row with the given id doesn’t exist, otherwise it will return the
      instance.
    - `.first_or_404()` will raise a 404 if the query does not return any results, otherwise it will return the
      first result.
    - `.one_or_404()` will raise a 404 if the query does not return exactly one result, otherwise it will
    ```python
    @app.route("/user-by-username/<username>")
    def user_by_username(username):
        # Description can be used to provide an optional custom error message to the 404
        user = db.one_or_404(
                db.select(User).filter_by(username=username),
                description=f"No user named '{username}'."
        )
        return render_template("show_user.html", user=user)
    ```

2. Use the `Flask.abort()` or `Flask.make_response()` methods to generate the error message.

For example:

@app.route('/cause-error')
def cause_error():

# Simulate an internal server error

abort(500, description="Internal Server Error: Simulated error")

```python
@app.delete('/regions/<code>')
def delete_region(code):
    """ Deletes the region with the given code.

    Args:
        param code (str): The 3-character code of the region to delete
    Returns:
        JSON If successful, otherwise abort with 404 Not Found
    """
    try:
        region = db.session.execute(db.select(Region).filter_by(NOC=noc_code)).scalar_one()
        db.session.delete(region)
        db.session.commit()
        return {"message": f"Region {noc_code} deleted."}
    except exc.SQLAlchemyError as e:
        # Optionally, log the exception
        app.logger.error(f"A database error occurred: {str(e)}")
        # Return a 404 error to the user who made the request
        msg_content = f'Region {noc_code} not found'
        abort(404, description=msg_content)
```

## Over to you

Try and add error handling to some of the routes.

## Optional: Configure Flask to handle errors and respond in JSON format

If you are writing a REST API or other routes that return JSON then you need to handle the errors by returning JSON
instead of views (templates).

The [Flask documentation](https://flask.palletsprojects.com/en/stable/errorhandling/#returning-api-errors-as-json) gives
examples for the following:

- Handle non-HTTP exceptions as 500 Server error in JSON format
- Return JSON instead of HTML for HTTP errors.
- Handle a specific HTTP error (404 in this case) with custom message for the app when Flask.abort() is called.

There are two approaches for how to define these in Flask:

1. Define the functions and use the `app.errorhandler()` decorator. You could then add them to your routes code.
2. Define the functions and in the Factory function, `create_app()`, register the error handlers.

### Approach 1: Define the functions using the `@app.errorhandler()` decorator

You can add the following the routes code, or a separate module for error handlers.

```python
from flask import json, current_app as app, jsonify
from werkzeug.exceptions import HTTPException


@app.errorhandler(Exception)
def handle_exception(e):
    """Handle non-HTTP exceptions as 500 Server error in JSON format."""

    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": 500,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.errorhandler(404)
def resource_not_found(e):
    """Handle a specific HTTP error (404 in this case) with custom message for the app when Flask.abort() is called.
    """
    return jsonify(error=str(e)), 404
```

### Approach 2: Define the error handling function and register it in the `create_app` factory function

The Flask documentation includes this in
the [Further Examples section](https://flask.palletsprojects.com/en/stable/errorhandling/#further-examples).

For example:

```python
def handle_404_error(e):
    """ Error handler for 404.

        Used when abort() is called. THe custom message is provided by the 'description=' parameter in abort().
        Args:
            HTTP 404 error

        Returns:
            JSON response with the validation error message and the 404 status code
        """
    return jsonify(error=str(e)), 404


def create_app(test_config=None):
    app = Flask('paralympics', instance_relative_config=True)

    # ... code removed here for brevity ...

    # Register the custom 404 error handler that is defined in this python file
    app.register_error_handler(401, handle_404_error)
```

## References

- [Python Exceptions](https://docs.python.org/3/tutorial/errors.html#exceptions)
- [W3Schools Try Except](https://www.w3schools.com/python/python_try_except.asp)
- [Handling application errors in Flask](https://flask.palletsprojects.com/en/stable/errorhandling/)
- [Handling exceptions in Flask-SQLAlchemy (Pretty Printed video series)](https://www.youtube.com/watch?v=P-Z1wXFW4Is)
