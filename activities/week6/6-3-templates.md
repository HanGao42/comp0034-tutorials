# Creating HTML templates in Flask

## How Flask uses HTML

Flask returns pages from a route using the `render_template` function.

This function takes an HTML template as a parameter.

By default, Flask looks for templates in a folder named `templates` in the application package.

Unlike Dash, in Flask you will have to write the HTML code.

## Activity: Create a route for the home, or index, page

The home page of a webs app is often referred to as the index.

1. Create a new file called `index.html` in the [templates folder](../../src/student/flask_paralympics/templates) of
   the Flask application. In PyCharm the HTML will be added for you, in VS Code you will have to add it yourself (copy
   the code from the [Boostrap CSS page](https://getbootstrap.com/docs/5.3/getting-started/introduction/#quick-start))
2. Add enough HTML to create a basic page e.g. add a paragraph tag in the body that says 'Welcome to HTML!':
   `<p>Welcome to HTML!</p>`.
3. Open the `paralympics_app.py` file and add `from flask import render_template` to the imports at the top.
4. Add, or modify, the app route associated with `"/"`
   URL. [See here](https://flask.palletsprojects.com/en/stable/quickstart/#a-minimal-application) for an example, though
   your function should be called `index()` and will return `return render_template('index.html')`
5. Run the app e.g. `flask --app student.paralympics_flask run --debug`. 
6. Go to the URL that is shown in the terminal e.g. <http://127.0.0.1:5000>
7. Check the page displays 'Welcome to HTML!' (or whatever you typed in index.html).
8. Stop the app using `CTRL+C`

## Apply styling using Bootstrap CSS
If you copied your HTML file from the Bootstrap page you may already have this.

### Adding an open source external CSS stylesheet in a Flask HTML template

While you can write your own CSS, **for your coursework it is recommended that you use a third party CSS**. Check it has
an open source license, i.e. that you are given permission by its author to use it. Writing your own CSS is not
considered in the mark scheme so writing your own CSS will not improve your marks.

Bootstrap is a popular CSS library that has extensive documentation and support and is used in the course materials for
this reason.

Bootstrap is widely used which some say leads to many sites looking similar, others criticisms include the fact that it
is comprehensive, leading to larger file sizes, and yet you may only want to use a small subset of its features. There
are alternatives to Bootstrap you can explore, try searching `alternatives to Bootstrap`, such as:

- [Pure.css](https://purecss.io/start/)
- [Materialize](https://materializecss.com/getting-started.html)

You can use a CDN (Content Distribution Network) version of Bootstrap, that is a version someone else hosts on their
server infrastructure. Refer to
the [Bootstrap documentation for the code you need to add](https://getbootstrap.com/docs/5.3/getting-started/introduction/#quick-start).
You need an active internet connection while your app is running to use this method. For this activity to avoid any
issues the current version (as at the time of writing) has been downloaded
from https://getbootstrap.com/docs/5.3/getting-started/download/

Flask apps have a folder named **static**. You place files that don't change while the app is running such as CSS,
JavaScript and images, in this folder. You can add sub-folders to **static**.

To reference the **static** folder in Flask, you use a Flask function `url_for` which you add using syntax for a Jinja
expression. Jinja is introduced in the next activity, for now please just accept the above syntax. The code structure is:

```jinja
<head>
   <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
</head>
```

`static` is the folder name, the `filename` should include both the .css file name and any sub-folder structure below
static. For example, if in a folder `static/css/mystyles.css` you would
use: `<link rel="stylesheet" href="{{ url_for('static', filename='/css/mystyles.css') }}">`

To apply Bootstrap styles to your HTML elements, you will need to refer to
the [Bootstrap documentation](https://getbootstrap.com/docs/5.3/getting-started/introduction/) and use the left side
menu to find the aspect you are interested in. This explains the bootstrap classes to use to achieve a particular
effect, and provides example code you can copy and adapt.

### Activity: Add Bootstrap CSS as the stylesheet to index.html

1. Open `index.html` in the `templates` folder.
2. Use the example above to work out what the `<link>` syntax should be for `bootstrap.css` within the `static/css`
   folder. Add this to the `<head>` section.
3. Use a [Boostrap style](https://getbootstrap.com/docs/5.3/content/typography/#inline-text-elements) to alter
   the `<p>Welcome to HTML!</p>` in some way, e.g. `<p class="text-decoration-underline">Welcome to HTML!</p>`
4. Run the app and check that the page styling has changed.

## Adapt the HTML and CSS to create a responsive template

### Intro to responsive design

The intent of responsive design is to make web pages look good on all devices: desktop, tablets, and phones. For
example, people are typically used to scrolling websites vertically but not horizontally. So there are techniques to
achieve responsive web design such as resize, hide, shrink, enlarge, move the content.

To create a web page that is responsive:

- Set the viewport
- Use responsive images
- Use responsive text
- Use media queries (apply a different style for different screen sizes)
- Optionally, use a grid layout

The **viewport** is the visible area inside the browser window. A `<meta>` viewport element gives the browser
instructions on how to control the page's dimensions and scaling. This gives the browser instructions on how to control
the page's dimensions and scaling. For example the following code would be placed in the `<head>` section of a html
document.

```html

<meta name="viewport" content="width=device-width, initial-scale=1">
```

- `width=device-width` sets the width of the page to follow the screen-width of the device (varies depending on the
  device).
- `initial-scale=1` sets the initial zoom level when the page is first loaded by the browser.

To use Bootstrap in a responsive way, the minimum you need is:

- Include the `<meta>` tag in the `<head>` to set the page width to the device
  `<meta name="viewport" content="width=device-width, initial-scale=1">`
- Wrap the page contents in an HTML `<DIV>` tag that has a container CSS class. Bootstrap offers two container classes:
    - `.container` class provides a responsive fixed width container
    - `.container-fluid` class provides a full width container, spanning the entire width of the viewport

### Activity: Update the HTML template to display the index page responsively

1. Open `index.html` in the `templates` folder.
2. In the `<head>` section before the style sheet
   add: `<meta name="viewport" content="width=device-width, initial-scale=1">`
3. In the `<body>` section add a `<div>` with a Bootstrap container class i.e. add `<div class='container'>` after `<body>`
   and `</div>` just before `</body>`
4. Add a large image within the `<div>` section
   using
   `<img src="{{ url_for('static', filename='/img/chart.png') }}" width="100%" alt="Paralympics line chart showing participants over time">`
5. Run the app and open it in a browser. 
6. Alter the size of the browser window, the image should re-size. 

[Next activity](6-4-jinja.md)
