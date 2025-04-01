# Creating Jinja templates in Flask

## Jinja references

The following references may be useful during this activity:

- [Jinja template designer documentation](https://jinja.palletsprojects.com/en/stable/templates/)
- [Flask tutorial on templates](https://flask.palletsprojects.com/en/stable/tutorial/templates/)
- [VS Code documentation on templates](https://code.visualstudio.com/docs/python/tutorial-flask#_create-multiple-templates-that-extend-a-base-template)
- [Primer on Jinja templating](https://realpython.com/primer-on-jinja-templating/)

## Overview of Jinja

### Syntax

Jinja is a template engine. You commonly use templates for web pages that receive dynamic content from
the back end, in this case the Flask application, and render it as a static page in the front end (web browser).

Jinja allows you to add elements to your page that will be generated from Python code.

Jinja templates can be HTML files that include Jinja syntax in them. The types of Jinja syntax you may want to use are:

- `{% ... %}` for statements such as `block` and `extends`; control structures `for` and `if`; and
  macros. [Macros](https://jinja.palletsprojects.com/en/3.1.x/templates/#macros) can be used to write reusable
  functions.
- `{{ ... }}` for expressions and variables
- `{# ... #}` for comments

Some examples of the syntax:

```jinja
{# To inherit all the layout from another template, in this case 'layout.html' #}
{% extends 'layout.html' %} 

{# To define an area, a 'block', in a template where the content will be dynamically provided for each page created from the template #}
{% block blockname %} 
    {# Here is where the dynamic contents will appear #}
{% endblock %}

{# For loop #}
{% for user in users %} 
	<p>{{ user.username|e }}</p> 
{% endfor %}
```

### Template inheritance

Jinja provides template inheritance. "Template inheritance allows you to build a base “skeleton” template that contains
all the common elements of your site and defines blocks that child templates can override."

In practical terms, in your Flask app you will create a parent template that contains the default HTML page structure, 
the CSS, etc. and then child templates inherit this and apply any specific changes for certain type of page.

If you then need to change the overall structure, e.g. a menu/nav bar or a CSS stylesheet, you only need to do so in 
one place, i.e. in the parent template.

### Escaping user input

In Flask, Jinja is configured to auto-escape any data that is rendered in HTML templates. This means that it’s safe to
render user input; any characters they’ve entered that could mess with the HTML, such as < and > will be escaped with
safe values that look the same in the browser but don’t cause unwanted effects. This will be important if you plan to
allow users to input text in some way in your application as it prevents them entering HTML script that could harm your
application.

## Create Jinja templates for the Paralympics app

### 1. Create a "parent" template that is the base page layout

This template will provide all the common elements of your web pages such as:

- the overall html structure
- links to css (and javascript) files
- defined sections that will have page specific content

You have already defined a Jinja2 variable `{{ variable }}` to use Flask `url_for` to render the path to the
CSS file.

Create a parent template in the templates folder with a meaningful filename such as `layout.html` or `base.html`. Add
the code below to it.

Create an empty file called `navbar.html` in the templates folder. You will edit this later.

The code includes the Bootstrap CSS and denotes sections that will be provided by 'child' templates:

- a **block** called `head` that will allow child templates to add to this if needed
- a **block** called `title` that allows child templates to set their own page title and inherits the overall website
  name
- an **include** that uses the contents of `navbar.html` to generate a navbar
- a **block** called content that will have the main page contents

You can add as many "block" elements as you wish with meaningful names to identify them.

This code has extra indents included to help you see the structure of the code. Your IDE is likely to remove
these indents!

```jinja2
<!DOCTYPE html>
<html lang="en">
    <head>
        {% block head %}
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="stylesheet" href="{{ url_for('static', filename='css/bootstrap.css') }}">
            <title>Paralympics - {% block title %}{% endblock %}</title>
        {% endblock %}
    </head>
    <body>
        <header>
            {% include 'navbar.html' %}
        </header>
        <div id="content" class="container-fluid">
            {% block content %}{% endblock %}
        </div>
        <!-- The following is the bootstrap JavaScript which is needed for some of the Bootstrap features -->
        <script src="{{ url_for('static', filename='js/bootstrap.js') }}"></script>
    </body>
</html>
```

### 2. Add Bootstrap navbar code to navbar.html

Create a basic Bootstrap navbar and save the code to the `navbar.html` template.

This file should contain just the HTML needed for
a [Bootstrap styled navigation bar](https://getbootstrap.com/docs/5.3/components/navbar/).

The code for the homepage link uses Jinja syntax to use the flask `url_for()` function to generate the link to the home
page of our app. The homepage route, '/', has the function name of 'index' in `paralympics_app.py`.

Links 1 and 2 do not currently have any pages to link to so will remain on the same page when clicked as denoted by
the '#' symbol.

```html

<nav class="navbar navbar-expand-lg bg-body-tertiary">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">Paralympics</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent"
                aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                <li class="nav-item">
                    <a class="nav-link active" aria-current="page" href="{{ url_for('index') }}">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Link 1</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">Link 1</a>
                </li>
            </ul>
        </div>
    </div>
</nav>
```

### 3. Create an `index.html` to inherit the parent template

`index.html` ia the name we will give to the home page template for the "/" route in the Paralympics app.

`index.html` inherits from `base.html` (or whatever name you saved it as) so all you need to provide is the values for
the **block**s.

Using `self.title()` in the [child template](https://jinja.palletsprojects.com/en/3.1.x/templates/#child-template)
allows access to a variable called `title` defined in a block elsewhere on the page.

Replace all the current contents of `index.html` with just the following:

```jinja2
{% extends 'base.html' %}

{% block title %}Home{% endblock %}

{% block content %}
    <p>This is the {{ self.title() }} page.</p>
{% endblock %}
```

### 4. Modify the route to call the template

Modify `routes.py` so the "/" returns `render_template('index.html')`.

### 5. Run the Flask app

Run the Flask app e.g. `flask --app student.paralympics_flask run --debug`

You should see a page with a nav bar that follows Bootstrap styling.

[Next activity](6-5-variable-routes.md)