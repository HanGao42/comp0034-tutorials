# Working with databases using Flask-SQLAlchemy

This week's activities introduce a different method for working with a SQL database using SQLAlchemy.

You do not have to use SQLAlchemy in a Flask app, however it is a commonly used approach and is included in the course
to give you experience of another way to access a database and experience of coding with Python classes.

This week's activities are likely to take longer than 2 hours.

If you prefer to continue using `sqlite3`, skip to activity 7.7.

## Overview of SQLAlchemy and Flask-SQLAlchemy

SQLAlchemy is a Python library for working with databases. It helps you manage and interact with databases by
allowing you to write Python code instead of SQL.

It is referred to as an ORM, object relational mapper. It provides a "mapping" between Python classes and database
tables.

[SQLAlchemy](https://www.sqlalchemy.org) allows you to use the same code with different databases, including SQLite.

[FlaskSQLAlchemy](https://flask-sqlalchemy.readthedocs.io/en/stable/) is an extension that provides extra features that make it easier to use SQLAlchemy in a Flask app.

Some of the syntax you will need is from Flask-SQLAlchemy, and some from SQLAlchemy. As a general rule, look at the
Flask-SQLAlchemy documentation first, if what you want is not covered there then move to teh SQLAlchemy documentation.

SQLAlchemy underwent a major revision at version 2.0 which changed the syntax for defining the Python classes (referred
to as models) and queries significantly. Take care when using SQLAlchemy tutorials written before January 2023 as they
will use the older style syntax, some of which is no longer supported or is deprecated. Deprecated means that you can
still use in the current release, but it is scheduled to be removed in a future release at which point your code would
no longer work.

## Using Flask-SQLAlchemy and SQLAlchemy in a Flask app

Make sure you installed FlaskSQLAlchemy, e.g. `pip install flask-sqlalchemy`. When you install it, it will install the
required version of SQLAlchemy also.

To use Flask-SQLAlchemy involves code in a number of areas of the Flask app.

### Code to create and configure the app

- Create an instance of Flask-SQLAlchemy object
- Configure it
- Initialise it for your Flask app
- Optionally, create the database tables.
- The object can then be used in the app when you want to interact with the database

In a Flask app any interaction has to be within a defined context. Code that is run in a route has a context. Database
interaction code that is outside a route, requires that you first create an application context. You will see examples
of this syntax in this activity.

### Code to map Python classes to database tables

You define classes and state how the Python class and attributes map to the database tables. You can specify a different
data type for the Python class than is stored in the database table. The Python class can also have operations (
functions).

Many of the tutorials you will see relating to the use of Flask-SQLAlchemy store the code to define the Python classes
in a module called `models.py`. This a convention, you do not have to name your module in this way.

### Code to interact with the database

The code for the routes will contain code that interacts with the database, though you can also have code in "helper"
functions that your routes import.

You use SQLAlchemy syntax that replaces direct SQL statements. Instead of working with rows, the data from rows is used
to create Python objects.

Activities 7.1 to 7.6 walk through how to apply this for the paralympics app.

[Next activity](7-2-initialise.md)
