# 3. Write tests that use Selenium webdriver to navigate elements on the page

## Introduction
This example uses the Selenium webdriver and the chrome driver, not requests, to navigate to a URL.

The driver allows you to navigate the web page and carry out actions such as clicking, selecting, entering data in forms
etc.

This is not an HTTP request so you will not get a response object back as you did in the last activity.
In the remaining activities you will use Selenium webdriver to find elements on a web page and then use pytest
assertions to compare values of those elements against an expected value.

You will likely need to refer to documentation to complete the activities:

- [Selenium documentation with examples](https://www.selenium.dev/documentation/webdriver/)
- [Selenium API reference](https://selenium-python.readthedocs.io/api.html)
- [Dash duo API functions (shorthand for some of the Selenium functions)](https://dash.plotly.com/testing#browser-apis)
- [HTML tag reference](https://www.w3schools.com/tags/default.asp)

## Concept: Dash duo functions versus Selenium Webdriver functions

Selenium webdriver provides functions that allow you to find elements on a page and then navigate them, e.g. by
clicking, entering text etc.

To use the Selenium functions use the `dash_duo.driver` and append the function Selenium e.g.
`dash_duo.driver.find_element(By.TAG_NAME, "h1")`

Dash has shorthand API functions for some Selenium webdriver functions, but not all. This can be confusing when you are
learning as you may see examples of both without understanding the difference. You do not have to use the Dash shorthand
version, you can use the Selenium syntax.

The Dash shorthand function are provided by the `dash_duo` fixture without the driver, e.g.
`dash_duo.find_element("h1")`.

## Concept: How to find an element on a page

Selenium WebDriver targets elements on the page. Dash uses the word 'component' rather than element. An element in this
context is something defined on the web page such as an HTML heading, an image, etc.

There are ways to identify (locate) elements on the page:

- by their HTML id
- by their CSS class or selector
- by HTML tag name
- by finding an element relative to another element
- by XPATH

See references for more detail:

- [Selenium locator strategies](https://www.selenium.dev/documentation/webdriver/elements/locators/)
- [Selenium methods to find elements](https://www.selenium.dev/documentation/webdriver/elements/finders/)

As an `id` has to be unique on an HTML page, this is the most convenient method. Use this where possible.

For example:

```python
from selenium.webdriver.common.by import By

# Code to create the driver is omitted

# Get the element with the id "fruit" using the Selenium function
fruit = dash_duo.driver.find_element(By.ID, "fruit")

# Using the Dash function alternative uses CSS selectors, so "#" before the id name denotes it is an ID
fruit = dash_duo.find_element("#fruit")
```

The Dash browser API finds elements by their CSS selector. These are:

- `#id` to find an element with an id, e.g. `#line-chart` to find an element with an id of 'line-chart'
- HTML TAG to find en element by its html tag name e.g. `p` to find all `<p>` elements
- .class to find an element by CSS class name, e.g. `.alert` to find all elements with a `class="alert"` (or
  className="alert" in Dash).

Using either API you can find either a single element `find_element`, or all elements that match a condition
on a page `find_elements`.

## Concept: Use an assertion on a value of the located element

The Selenium Webdriver API provides browser automation capability, it relies on a testing library for the test
capability. You therefore use the assertions for the testing library you choose e.g. pytest.

You are already familiar with pytest assertions.

Having used the webdriver to find an element, you some value from that in an assertion.

Examples of the values you can get from the webdriver to use in assertions:

```python
# Get browser information
title = driver.title
url = driver.current_url
# Get information about an element e.g. 
value = driver.find_element(By.CSS_SELECTOR, "input[type='checkbox']:first-of-type").is_selected()
# Get text content from an element
text = driver.find_element(By.CSS_SELECTOR, "h1").text
```

## Writing the test
### Test that checks the text content of the H1 heading

This example waits until an element, the 'h1' heading appears, rather than waiting a set amount of time as was used in
the previous test. It then checks that the heading text is 'Paralympics Dashboard'.

```python
from dash.testing.application_runners import import_app


def test_home_h1_text_equals(dash_duo):
    """
    GIVEN the app is running
    WHEN the home page is available
    THEN the H1 heading with an id of 'title' should have the text "Paralympics Dashboard"
    """
    # As before, use the import_app to run the Dash app in a threaded server
    app = import_app(app_file="student.dash_single.paralympics_dash")
    dash_duo.start_server(app)

    # Wait for the H1 heading to be available on the page, timeout if this does not happen within 4 seconds
    dash_duo.wait_for_element("h1", timeout=4)  # Dash function version

    # Find the text content of the H1 heading element
    h1_text = dash_duo.find_element("h1").text  # Dash function version

    # Assertion checks that the heading has the expected text
    assert h1_text == "Paralympics Dashboard"
```

Run the test.

### Further tests

Try and identify at least one more similar test that finds an element on a page and then asserts a value from that
element. For example, find the dropdown selector and check it has one of the expected values (events, sports,
countries).

[Next activity](4-4-interactions.md)