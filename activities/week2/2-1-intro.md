# Tutorial 2: Creating and adding charts to a Dash app

## Introduction

In this tutorial you will learn to create and add charts to a Dash app layout. You will then replace the chart images
you added to the chart last week with charts generated from the paralympics data.

Next week you will add the callback functionality that will allow the charts to be dynamically updated.

The activities this week assume you are using the single page app in paralympics_dash.

You can apply the same to the same charts in the multi-page app by editing the layouts in the pages rather than the main
dashboard python file.

## Plotly graphing library for Python

Plotly graphing library for Python has two packages within it, Plotly Express and Plotly Go.

Plotly Express provides Python classes and functions to create most types of charts, and in most cases will be
sufficient for the coursework.

If you need to edit aspects of a chart that are not available through Express functions, use Go instead.

Many of the chart examples in the [Plotly documentation](https://plotly.com/python/) start with an Express example, then
show
features that require Go. They also include a version that can be added to a Dash app.

## Choosing the type of chart

The Plotly documentation shows examples of code for many types of chart, however this assumes you already know the type
of chart you want to create. To help you decide which type of chart may be suited to your particular data and audience,
then try one of the many tools to help you select the type of chart/data visualisation:

- [Data Visualisation Catalogue](https://datavizcatalogue.com/index.html)
- [Depict Data Studio](https://depictdatastudio.com/charts/)
- [Page with links to other chart choosers](https://coolinfographics.com/dataviz-guides)

## Creating a chart

The general approach to create and add a chart to a Dash application is:

1. Access the required data
2. Create a chart object using the data
3. Add the chart object to the Dash app layout

## This week's activities

This week's activities cover the data visualisations listed in the table below.

The examples use 2 different ways to access the data. The purpose of this is to introduce different ways of accessing
the data. For your coursework don't do this, pick one method to access the data.

| Activity                         | Chart type                                       | Data access method       | Chart library  |
|:---------------------------------|:-------------------------------------------------|:-------------------------|:---------------|
| [Activity 1](2-2-line-chart.md)  | Line chart                                       | pandas / .csv            | Plotly Express |
| [Activity 2](2-3-bar-chart.md)   | Bar chart                                        | pandas / .csv            | Plotly Express |
| [Activity 3](2-4-scatter-map.md) | Scatter geo map with markers                     | pandas / SQLite database | Plotly Express |
| [Activity 4](2-5-stats-card.md)  | Summary statistics presented in a Bootstrap card | pandas / SQLite database | None           |

## Check the paralympics app runs

Check that the app as at the end of week 1 runs:

1. Open `src/student/dash_single/paralympics_dash.py` and run the app.
2. Go to the URL that is shown in the terminal. By default, this is <http://127.0.0.1:8050>.

If you did not complete the activities in week 1, then you may need to copy and adapt the code from the tutor solution
into the `paralympics_dash.py` file.

Go to GitHub; update your fork; then in your IDE pull the changes from GitHub to your local repository. This will pull
in any changes from the src/tutor source tree.

A completed version of week 1 is in the `paralympics_dash_1.py` file.

[Next activity](2-2-line-chart.md)