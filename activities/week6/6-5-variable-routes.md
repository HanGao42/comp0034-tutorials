# Routes with variables & HTTP methods

## Routes with variables

You can add variable sections to a URL by marking sections with `<variable_name>`. Your function then receives the
`<variable_name>` as a keyword argument. Optionally, you can use a converter to specify the type of the argument
like <converter:variable_name>.

See Flask documentation: [Variable routes](https://flask.palletsprojects.com/en/stable/quickstart/#variable-rules)

### Task: Add a variable to the index route

Make the "index" route accept a variable that allows the user to enter their name and a personalised
homepage message e.g. 'Hello _name_ and welcome to the paralympics app'.

To test it, run the app and pass the name when you enter the URL e.g. `http://127.0.0.1:5000/Fred`

## Routes that support other HTTP methods

By default, if you do not specify the HTTP method that a route accepts then it will be a GET route.

To specify that a route accepts more than one method you add them like this:

```python
@app.route('/login', methods=['GET', 'POST'])
```

Alternatively there are shorthand variants for each HTTP method:

```python
@app.get('/login')
@app.post('/login')
@app.delete('/remove')
@app.put('/update')
```

Refer to the [documentation](https://flask.palletsprojects.com/en/stable/quickstart/#http-methods) for further info.

When you enter a URL in a browser it is treated as a GET request. To submit URLs that are POST or other type of requests
will need a method that allows you to specify the HTTP method type, such as using
the [HTTPie python library](https://github.com/httpie/cli) or trying the developer tools in Chrome:

- Open DevTools (Ctrl+Shift+I)
- Go to the "Network" tab
- Select the "Fetch/XHR" sub-tab
- Click the "New Request" button
- Enter the URL you want to send the POST request to
- Change the method dropdown from "GET" to "POST"
- Click the "Payload" tab to add the POST body
- Click the "Send" button to execute the request

Later tutorials will have examples of POST routes.
