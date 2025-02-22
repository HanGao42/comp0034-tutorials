# Flask message flashing

Flask's [message flashing](https://flask.palletsprojects.com/en/stable/patterns/flashing/#message-flashing) system can
be used to provide feedback to users.

The flashing system basically makes it possible to record a message at the end of a request and access it next request
and only next request.

## Steps to implement Flash messages

The basic steps:

- Import the necessary modules (flash, get_flashed_messages)
- Set up a secret key (NB: you already have a SECRET_KEY in `__init__.py`)
- Create routes that use flash to send messages
- Modify the templates to display flashed messages. The `base`/`layout` template is usually modified to add this so it
  is available to any template that inherits it.

## Try it

1. Add the following route to the paralympics app.

    ```python
    from flask import flash, redirect, url_for
    
    
    @main.route('/flash')
    def flash_message():
        # Generate a Flash message
        flash('This is a flash message!')
        # Redirect to the homepage, the flash message should be displayed
        return redirect(url_for('main.index'))
    ```
2. Modify the base template. You may have named it `base.html` or `layout.html`.

    ```html
    <!-- Add to the body section of your base/layout template -->
    <body>
    {% with messages = get_flashed_messages() %}
    {% if messages %}
    <ul>
        {% for message in messages %}
             <li>{{ message }}</li>
        {% endfor %}
    </ul>
    {% endif %}
    {% endwith %}
    </body>
    ```
3. Run the Flask application
4. Trigger Flash messages by navigate to the root URL then add `/flash` and press enter. You should redirect to the home
   page with a flash message visible.

## Extension

Customize the flash messages with
different [categories (e.g., success, error)](https://flask.palletsprojects.com/en/stable/patterns/flashing/#flashing-with-categories)
and style them using [CSS](https://getbootstrap.com/docs/5.3/utilities/colors/#colors).

[Next activity](7-9-errors.md)