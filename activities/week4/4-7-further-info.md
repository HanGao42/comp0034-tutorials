# 7. Further information

## Links to other tutorials

[Building unit tests for dash applications](https://plotly.com/blog/building-unit-tests-for-dash-applications/). This
goes beyond what is expected for the coursework and tests callbacks and uses mocks. Useful if you want to expand your
knowledge.

[Plotly Dash Testing official documentation](https://dash.plotly.com/testing)

Dash have [tests for their code in GitHub](https://github.com/plotly/dash/tree/dev/tests). It can be useful
to see how they structure their own tests.

[Sean McCarthy's Dash testing tutorial](https://mccarthysean.dev/005-03-Dash-Testing). He uses the dash_thread_server
and dash_br fixtures rather than dash_duo, however it gives a number of examples of different ways to select elements on
the page for testing.

## Python playwright - an alternative to using Selenium Webdriver

If you do not wish to use Selenium Webdriver, an accepted alternative for the coursework
is [Python playwright](https://playwright.dev/python/docs/intro).

Some students last year preferred this as it seemed to avoid issues with browser driver versions and waits.

Playwright locators are different to Selenium so you will need to read their documentation and find tutorials. 
Try [Pytest with Eric's Playwright tutorial](https://pytest-with-eric.com/automation/pytest-playwright/).

A minimal example for the paralympics Dash app:

```python
""" Minimal example of a test using Python playwright instead of Selenium webdriver

Install the playwright and pytest-playwright packages with pip:
pip install pytest-playwright playwright

"""
import pytest
from dash.testing.application_runners import import_app
from playwright.sync_api import expect, sync_playwright


@pytest.fixture(autouse=True)
def start_app(dash_duo):
    """ Pytest fixture to start the Dash app in a threaded server.
    This is a function-scoped fixture.
    Automatically used by all tests in this module.
    """
    app_file_loc = "tutor.dash_single_t.para_single_wk3"
    app = import_app(app_file_loc)
    yield dash_duo.start_server(app)


@pytest.fixture()
def app_url(start_app, dash_duo):
    """ Pytest fixture for the URL of the running Dash app. """
    yield dash_duo.server_url


def test_h1_text_equals(app_url):
    """
    GIVEN the app is running
    WHEN the home page is available
    THEN the H1 heading with an id of 'title' should have the text "Paralympics Dashboard"
    """

    with sync_playwright() as p:
        # Uses the Chrome browser, see https://playwright.dev/python/docs/browsers#google-chrome--microsoft-edge
        browser = p.chromium.launch(channel="chrome")
        page = browser.new_page()

        # Go to the home page of the app
        page.goto(app_url)

        # Check that the h1 heading which has the id="title" has the expected text
        expected_text = "Paralympics Dashboard"
        title = page.locator("#title")
        expect(title).to_have_text(expected_text)

        browser.close()

```
