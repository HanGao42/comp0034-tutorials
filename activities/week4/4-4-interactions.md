# 4. Write tests that involve interactions such as click or entering text

## Introduction

In the previous test you found a heading, located the text value and then used an assertion to check that value.

In most end-to-end tests you are likely to be testing a behaviour that would typically involve interactions from the end
user.

For example take the following user story:

```text
As a student, I want to see a chart showing the number of male, female and total participants per year, so that I can
analyze the participation trends athletes by gender.

Acceptance Criteria:

- Display a bar chart showing the number of male, female and total participants for each year.
- Allow filtering by Summer or Winter games.
- Provide tooltips with detailed information when hovering over data points.
```

To test this fully might require that we:

- Find the bar chart
- Select a filtering option
- Hover over a tooltip for a given data point

To do this, you need to interact with elements such as click on a checkbox and hover over a data point. Selenium allows
you to do this.

## Concept: Interacting with elements on a web page

[Selenium documentation: Interactions](https://www.selenium.dev/documentation/webdriver/elements/interactions/)

Basic commands for interacting include click(), send_keys(), clear(), select().

For example, to complete and submit a form with a first-name field:

```python
from selenium.webdriver.common.by import By

# Find the element
first_name = driver.find_element(By.name, "first-name")
# Enter the text "Charles"
first_name.send_keys("Charles")
# Fina and click on the form submit button
driver.find_element(By.TAG_NAME, "input[type='submit']").click()
```

## Concept: Waits

When you use Selenium functions to navigate the page and interact with elements, you may need to wait for the page to
respond or update before you can continue. A test may execute faster than the browser responds. So, if you don't wait
you may get an error that is not a problem with the app, only that the element you were looking for hadn't yet loaded.

You can use waits to wait for an element to load before you try to interact with it.

There are two types of waits in Selenium:

- explicit [waits](https://www.selenium.dev/documentation/en/webdriver/waits/)
  for [an expected condition](https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html?highlight=expected)
  to be true, e.g., until a particular element is displayed.
- implicit [waits](https://www.selenium.dev/documentation/webdriver/waits/#implicit-waits) that wait for a specific
  period.

```python
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Implicit wait for 2 seconds
driver.implicitly_wait(2)

# Wait for 10 seconds until the element with ID of "myElement" is present on the web page
# General syntax for explicit wait: WebDriverWait(driver, timeout=int_in_seconds).until(some_condition)
element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "myElement")))
```

The Dash API also offers the following wait functions:

- `wait_for_element(selector, timeout=None)`: shortcut to wait_for_element_by_css_selector the long version is kept for
  back compatibility. timeout if not set, equals to the fixture's wait_timeout
- `wait_for_element_by_css_selector(selector, timeout=None)`: explicit wait until the element is present, shortcut to
  WebDriverWait with EC.presence_of_element_located
- `wait_for_element_by_id(element_id, timeout=None)`: explicit wait until the element is present, shortcut to
  WebDriverWait with EC.presence_of_element_located
- `wait_for_style_to_equal(selector, style, value, timeout=None)`: explicit wait until the element's style has expected
  value. shortcut to WebDriverWait with custom wait condition style_to_equal. timeout if not set, equals to the
  fixture's wait_timeout
- `wait_for_text_to_equal(selector, text, timeout=None)`: explicit wait until the element's text equals the expected
  text. shortcut to WebDriverWait with custom wait condition text_to_equal. timeout if not set, equals to the fixture's
  wait_timeout
- `wait_for_contains_text(selector, text, timeout=None)`: explicit wait until the element's text contains the expected
  text. shortcut to WebDriverWait with custom wait condition contains_text condition. timeout if not set, equals to the
  fixture's wait_timeout
- `wait_for_class_to_equal(selector, classname, timeout=None)`: explicit wait until the element's class has expected
  value. timeout if not set, equals to the fixture's wait_timeout. shortcut to WebDriverWait with custom class_to_equal
  condition.
- `wait_for_contains_class(selector, classname, timeout=None)`: explicit wait until the element's classes contains the
  expected classname. timeout if not set, equals to the fixture's wait_timeout. shortcut to WebDriverWait with custom
  contains_class condition.
- `wait_for_page(url=None, timeout=10)`: navigate to the url in webdriver and wait until the dash renderer is loaded in
  browser. use server_url if url is None

You can also use other Python libraries to introduce a wait, e.g. `time.sleep(2)` would halt the test from running for 2
seconds. This can be useful if you want to wait before the driver has been initialised.

## Writing the tests
### Write a test that when you click on a checkbox that the bar chart updates
The test specification is:
```text
GIVEN the app is loaded
AND a checkbox is present on the page
AND a bar chart is displayed on the page
WHEN the checkbox selection is changed
THEN the chart should be updated
```

You will need to decide how to assert that the chart has updated. For example, check the number and ids of the chart
elements in the column that contains the bar charts.

In the tutor week 3 single page Dash app, by default the summer bar chart is selected, so if the second box is selected
then a second chart should be in the div.

One possible structure for the test:

```python
def test_bar_chart_updates(dash_duo):
    """
    GIVEN the app is running
    AND the checkboxes are present on the page
    AND a bar chart is present on the page
    WHEN both checkboxes are selected
    THEN the two charts should be in the div with the id 'bar-div' (can be tested with the class=dash-graph)
    """

    app = import_app(app_file)
    dash_duo.start_server(app)

    # Wait until the checkbox element is displayed

    # Find div with the id 'bar-div' that contains the charts

    # count the number of elements in bar_div with the class 'dash-graph'

    # Select the 'Winter' checkbox. Summer is already selected by default.

    # Click the checkbox

    # Wait 2 seconds for the bar chart to update

    # Find div with the id 'bar-div' that contains the charts again

    # count the number of elements in bar_div with the class 'dash-graph'
    
    # There should be 2 charts now and 1 at the start so you can assert that num_charts_after > num_charts_before

```

Implement the code and run the test.

[Next activity](4-5-complex-selector.md)