# 2. Configure the webdriver, run the app and write a test to verify that the app is running

This activity tests that you can reach the main page of Dash app (in a single page app there is only one page!).

## Configure the selenium webdriver for chrome

This assumes you already completed the testing intro activity and have downloaded a chrome driver to your computer.

Selenium creates an instance of a webdriver object for the browser, in this case Chrome. This webdriver in turn uses the
ChromeDriver software you installed earlier.

Add the following code to `conftest.py`. This is not a pytest fixture. pytest will automatically
use anything in `conftest.py`, its use is not restricted to fixtures. The code below sets configuration "options" for
the webdriver.

When you run tests on GitHub Actions there is no monitor with a browser so you run the Chrome browser in a mode called
"headless".

However, if you want to run the tests on your computer and see what is happening then you do not want "headless". You
also need to have the browser set large enough that it can find elements of your page. A good starting point is to
maximise the browser window.

The following code handles this for you, it will detect if its being run on GitHub Actions and if so will set 
"headless" mode, otherwise it will run in a maximised browser window.

```python
import os
from selenium.webdriver.chrome.options import Options


def pytest_setup_options():
    """pytest extra command line arguments for running chrome driver

     For GitHub Actions or similar container you need to run it headless.
     When writing the tests and running locally it may be useful to
     see the browser and so you need to see the browser.
    """
    options = Options()
    if "GITHUB_ACTIONS" in os.environ:
        options.add_argument("--disable-gpu")
        options.add_argument("--no-sandbox")
        options.add_argument("--headless")
    else:
        options.add_argument("start-maximized")
    return options
```

## Use the dash_duo fixture to run the Dash app

The `dash_duo` test [fixture](https://dash.plotly.com/testing#fixtures) is used to run the Dash app in a local server
for testing. This assumes that you have installed `dash[testing]`. It runs on a thread. Threads are used to allow more
than one process to run concurrently, in this case you need to run the Dash app and run the test code at the same time.

Plotly Dash [test documentation examples](https://dash.plotly.com/testing#end-to-end-tests) define the app to be tested
inside each test case which is impractical for our purposes.

[This post in the plotly forum](https://community.plotly.com/t/how-you-can-integration-test-your-app-by-dash-testing/25002)
which recommends using a function called `import_app` which is imported from `dash.testing.application_runners`.

I have not found any examples or documentation of creating the app as a pytest fixture that is only run once per
session.
It relies on the `dash_duo` fixture which has a function scope (i.e. created once for each test function).

You need to explicitly start the server, though there is no method to stop the server, this is handled by the fixture at
the end of each test.

An example of how to do this within a test for the paralympics_dash app where the package name is `student.dash_single`
and the module that runs the Dash app is `paralympics_dash.py`:

```python
from dash.testing.application_runners import import_app


def test_server_live(dash_duo):
    # Create the app
    app = import_app(app_file="student.dash_single.paralympics_dash")
    # Start the server with the app using the dash_duo fixture
    dash_duo.start_server(app)

    # test code will follow here
```

Note: It causes issues when trying to create the app in the tests if the Python package and the Python module that runs
the app have the same name. You will need to rename the package or module if this applies to you.

## Write a test to check that the server is up and running using the Python requests library

You can specify which URL to run the server on. However, to avoid needing to know this, the following code gets the
server url from the running test app and then uses that in the test. This is important when using GitHub Actions
where you cannot control the port number.

The Python requests library is used to make an HTTP request to the server. This returns
a [response object](https://www.w3schools.com/python/ref_requests_response.asp). A response object's properties include:

- status_code: the [HTTP status code](https://www.w3schools.com/tags/ref_httpmessages.asp)
- content: in bytes. This is the content returned by the URL, in this case the Dash app page HTML.
- text: The page content in text format (unicode).
- headers: the HTTP headers which includes Content-Type
- json(): if the URL returns JSON such as an API this can be useful

You can then use pytest assertions to check for a condition in any of the components of the response object. In this
case, check that HTTP status code is 200 for success.

Create a test module in the tests directory, e.g. `test_paralympics_dash.py`, and add code to test that the server is
live.

It will look something like this:

```python
import requests
from dash.testing.application_runners import import_app


def test_server_live(dash_duo):
    """
    GIVEN the app is running
    WHEN an HTTP request to the home page is made
    THEN the HTTP response status code should be 200
    """

    # Start the app in a server
    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # Delay to wait 2 seconds for the page to load
    dash_duo.driver.implicitly_wait(2)

    # Get the url for the web app root
    # You can print this to see what it is e.g. print(f'The server url is {url}')
    url = dash_duo.driver.current_url

    # Requests is a python library and here is used to make an HTTP request to the sever url
    response = requests.get(url)

    # Finally, use the pytest assertion to check that the status code in the HTTP response is 200
    assert response.status_code == 200
```

Run the test e.g. `pytest -v` in a terminal, or use a run test function in your IDE.

[Next activity](4-3-locate-elements.md)
