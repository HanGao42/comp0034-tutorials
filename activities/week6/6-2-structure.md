# Flask app structure and configuration

## Moving to a package structure

The first example used a Flask app with a basic structure.

A single Python file contains the code to create an instance of a Flask app and define app's routes.

While this worked for the simple example, as the app grows the structure will become inflexible and create a monolithic
file that breaks the principles of a good design.

A more
typical [Flask application structure is to define packages](https://flask.palletsprojects.com/en/stable/patterns/packages/).
This is what you should aim for in your coursework. Note that if you created a copy of the GitHub classroom coursework
assigment this puts the "/flaskappname" part of the directory tree within an "src" folder.

The file and folder structure will look something like this:

```text
/your_project_name
    /.instance
        database.db  (Flask instance folder with the database)
    /flask_app_name
        __init__.py (you will define a function here that creates and configures the Flask app object)
        models.py  (Python classes that map to the SQL database tables)
        routes.py  (Flask routes)
        helpers.py (helper functions used in the routes)
        /static
            /css
                (Bootstrap css files)
            /js
                (Bootstrap JavaScript files)
        /templates
            layout.html
            index.html
            ... any other HTML templates
    /tests
        conftest.py
        test_some_name.py
        ... and any other test files
    .venv/
    pyproject.toml
    requirements.txt
```

This is not the only structure you can use. For example, you may see examples that separate the app into packages and
use Flask Blueprints to 'modularise' the functionality.

## Creating the app using the Factory pattern

Remember the design patterns lecture? No, well, there is a design pattern called Factory.

Flask uses a pattern called
the [application factory](https://flask.palletsprojects.com/en/stable/patterns/appfactories/) for creating and
configuring Flask apps.

Like a factory production line, you create the Flask app object, then you pass it along a production line adding extra
"features" to it as needed. You can dynamically decide on what to add as you create the app.

## Step 1: Create a function in the flask_paralympics package's `__init__.py` to create and configure the app instance

When a package is imported, the `__init__.py` is implicitly executed and any objects it defines are bound to the package
namespace.

If you create the Flask object in the `__init__.py` it is then a global variable that is available to other modules in
the package.

Creating the app using the application factory pattern lets you create the app and then flexibly add configuration to
it. You need to be able to do this for some of the packages that you will use to create your app.

1. Open `src/student/flask_paralympics/__init__.py`
2. Add a function that must be named `create_app`. The code below is based on the `create_app()` function from
   the [Flask tutorial application setup](https://flask.palletsprojects.com/en/stable/tutorial/factory/#application-setup)
   without the routes. The routes will be in a separate python module, currently the `routes.py` file.:

   ```python
    import os

    from flask import Flask


    def create_app(test_config=None):
        # create the Flask app
        app = Flask(__name__, instance_relative_config=True)
        # configure the Flask app (see later notes on how to generate your own SECRET_KEY)
        app.config.from_mapping(
            SECRET_KEY='dev',
            # Set the location of the database file called paralympics.sqlite which will be in the app's instance folder
            SQLALCHEMY_DATABASE_URI= "sqlite:///" + os.path.join(app.instance_path, 'paralympics.sqlite'),  
        )

        if test_config is None:
            # load the instance config, if it exists, when not testing
            app.config.from_pyfile('config.py', silent=True)
        else:
            # load the test config if passed in
            app.config.from_mapping(test_config)

        # ensure the instance folder exists
        try:
            os.makedirs(app.instance_path)
        except OSError:
            pass

        return app
    ```

## Step 2: Add necessary configuration parameters for the Flask app

Flask has several ways you can [define configuration parameters](https://flask.palletsprojects.com/en/stable/config/)
for the Flask app. You can use any method.

Some of the package extensions you will use rely on configured parameters.

### `SECRET_KEY`

`SECRET_KEY` is a configuration parameter used by Flask and extensions to keep data safe.

It's set to "dev" in the code you just added to provide a convenient value during development, but it should be
overridden with a random value when deploying the app.

You can generate a secret key from the Terminal command line. Type `python3` or `python` and press enter. At
the `>>>` prompt type `import secrets` and press enter. Then type `secrets.token_urlsafe(16)` and press enter. You
should see a string of 16 characters. Copy this and use it to replace the word 'dev' in
the SECRET_KEY line in the `create_app()` function.

![Create a SECRET_KEY](../img/secret_key.png)

### `SQLALCHEMY_DATABASE_URI`

`SQLALCHEMY_DATABASE_URI` is the path where the SQLite database file will be saved. It's under `app.instance_path`,
which is the path that Flask has chosen for the instance folder and by default will be created the first time you run
the app. The instance folder is created just outside the app's package directory.

You can change the database location to any other directory by changing the `SQLALCHEMY_DATABASE_URI`.

## Step 3: Modify the current app code to use the create_app() function

Now that the app is created in the `create_ap()` function, you need to modify the file where you first created the app (
e.g. `paralympics_app.py`) to use this.

A commonly used approach is to define the routes and assign them to a
Blueprint. [Blueprints](https://flask.palletsprojects.com/en/stable/blueprints/) are a concept or pattern in Flask to
assist in structuring code to make it potentially easier to modularise large applications.

You define a Blueprint and assign routes to it. You then register the Blueprint on the Flask app after it is
initialised, i.e. in the `create_app()` function.

An alternative to using a Blueprint is to use Flask's `current_app` object to access the configured app. For example,
using `import current_app as app` accesses the current app and names it `app` so that you don't have to change the
routes which already refer to `@app`.

To apply the Blueprint approach in the paralympics app, change the contents of `routes.py` (or whatever file name you
used for the routes code) in the following ways:

1. Add the import `from flask import Blueprint`
2. Remove the import `from flask import Flask`
3. Add a line of code before the route functions to define a Blueprint: `main = Blueprint('main', __name__)`
4. Delete the code that creates the app instance (`app = Flask(__name__)`)
5. Modify the route definitions to start `@main.route` instead of `@app.route`
6. Delete the code that runs the app (`if __name__ == '__main__': app.run(debug=True)`)

You should then just have the code that defines the routes, e.g.

```python
from flask import Blueprint

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return f"Hello!"
```

## Step 4: Update the `create_app()` function to register the app's routes

Return to the `create_app()` function and now let the app know about the routes that are defined in `paralympics.py`.

You do this by registering the Blueprint. To avoid circular imports you need to add the import within the create_app()
function.

```python
# Put the following code inside the create_app function after the code to ensure the instance folder exists
with app.app_context():
    # Register the blueprint
    from student.flask_paralympics.routes import main

    app.register_blueprint(main)
```

The concept of application contexts isn't covered right now but for those who want to know more,
see [Patrick Kennedy's blog](https://testdriven.io/blog/flask-contexts-advanced/).

Check that you can run the app modifying the command to use just the package name 'student.flask_paralympics':

```terminal
flask --app student.flask_paralympics run --debug
```

Flask finds and recognises the `create_app()` function as it is in the `__init__.py` of the student.flask_paralympics
package, and it conforms to the expected function name (create_app).

[Next activity](6-3-templates.md)
