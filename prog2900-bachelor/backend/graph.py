#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
graph: Module consisting of functions that generate HTML pages with embedded code to deliver plots
        as they appear in CIE Functions.

Copyright (C) 2012-2020 Ivar Farup and Jan Henrik Wold
Copyright (C) 2024 Bachelor Thesis Group 8

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

"""
    graph.py, module for creation of plot endpoints.
    Achieves this by dynamically creating a HTML page with embedded JS code to construct the plots
    and add functionality through checkboxes. This module is loosely based on the original plotting module,
    https://github.com/ifarup/ciefunctions/blob/master/tc1_97/plot.py .

    This module contains one instance of code lent from the internet, in the form of a transpose function
    for the embedded JS code. These are marked with '// from StackOverflow, see module description.'.
    The code is from this StackOverflow answer:
    https://stackoverflow.com/a/36164530

"""
import json
import sys
from array import array
import numpy as np

import cieapi
from computemodularization import compute_LMS_modular, compute_MacLeod_modular, compute_Maxwellian_modular, \
    compute_XYZ_modular, \
    compute_XY_modular, compute_XYZ_purples_modular, compute_xyz_standard_modular, compute_XYZ_standard_modular, \
    compute_xyz_purples_modular

def checkboxes(graph_function):
    """
    checkboxes() is a function that constructs the HTML checkboxes, making them enabled/disabled
    depending on the function in question (as some have different needs than others).

    Parameters
    ----------
    graph_function: Either a:
        - Function for plotting a certain calculation.
        - A string that represents the field_size and standardization function for the four unique instances
            a user can use them (having to be different due to them using the same functions.)

    Returns
    -------
    A string representing the HTML for the page, with a div for the plot and a series of checkboxes.

    """
    # "disabled" represents the four possible checkboxes,
    # compare to cie1931
    # compare to cie1964
    # turn on/off grid
    # turn on/off labels
    # some functions have some enabled/disabled; this routes that process
    disabled = []
    if graph_function in [LMS_graph, XYZP_graph]:
        disabled = [False, False, True, False]
    if graph_function in [maxwellian_graph, macleod_graph, xyp_graph]:
        disabled = [False, False, True, True]
    if graph_function == XYZ_graph:
        disabled = [True, True, True, False]
    if graph_function == XY_graph:
        disabled = [True, True, True, True]
    if graph_function == "cie1931_2":
        disabled = [False, True, True, False]
    if graph_function == "cie1964_10":
        disabled = [True, False, True, False]
    if graph_function == "xyz1931_2":
        disabled = [False, True, True, True]
    if graph_function == "xyz1964_10":
        disabled = [True, False, True, True]

    # html representations of each of these checkboxes
    templates = ['<input type="checkbox" id="cie1931" name="cie1931"',
                 '<input type="checkbox" id="cie1964" name="cie1964"',
                 '<input type="checkbox" checked id="grid" name="grid"',
                 '<input type="checkbox" id="label" name="label"']

    # goes through them, checking if they're enabled or disabled, disables them by adding the 'disabled' semantic
    for input in range(len(templates)):
        if not disabled[input]:
            templates[input] += " disabled>"
        else:
            templates[input] += ">"

    # standard template for adding all of them
    standard = """
    <div id="inputrow">
        <span>
        <label for="cie1931">Compare with CIE 1931 2°</label>
        """ + templates[0] + """
        </span>
        <span>
        <label for="cie1931">Compare with CIE 1964 10°</label>
        """ + templates[1] + """
        </span>
        <span>
        <label for="cie1931">Grid</label>
        """ + templates[2] + """
        </span>
        <span>
        <label for="cie1931">Labels</label>
        """ + templates[3] + """
        </span>
    """

    # the LMS function has the logarithmic values button that can be added
    if graph_function == LMS_graph:
        standard += """
        <span>
            <label for="log">Logarithmic values</label>
            <input type="checkbox" id="log" name="log">
        </span>
        """
    # returns it enclosed within the div
    return standard + " </div>"


def retrievePoints(func, param):
    """
    retrievePoints() creates a range of numbers for points on specific plots.
    Parameters
    ----------
    func: graph function in usage
    param: parameters from the global parameter system within backend

    Returns
    -------
    A series of unique numbers that all represent the wavelength for points on specific graphs.

    """
    # does this weird setup to remove potential duplicates

    if func == macleod_graph:
        initial = list(set([int(param['min']), 410, 420, 430, 440, 450, 460, 470, 480, 490, 500, 550, 575, 600, 700,
                            int(param['max'])]))
        return initial
    if func == maxwellian_graph:
        initial = list(
            set([int(param['min']), 450, 460, 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610,
                 620, 630, 700, int(param['max'])]))
        return initial
    if func == XY_graph:
        initial = list(
            set([int(param['min']), 470, 480, 490, 500, 510, 520, 530, 540, 550, 560, 570, 580, 590, 600, 610, 700,
                 int(param['max'])]))
        return initial


def head(function):
    """
    head(), creates the start of the HTML output by adding embedded plotly and CSS for some effects,
    also initializes the checkboxes() for each function.
    Parameters
    ----------
    function: The graph function to be used for checkboxes.

    Returns
    -------
    String representing HTML for the start of the total HTML output.
    """

    return """
    <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <script src='https://cdn.plot.ly/plotly-2.32.0.min.js'></script>
    <style>
        #plot {
            border: 1px solid black;
        }
        #plot * {
            margin-left: auto;
            margin-right: auto;
        }
        #inputrow {
            display: flex; 
            flex-direction: row;
            justify-content: space-around;
        }
    </style>
</head>
<body>
    <div id='plot'></div>
    """ + checkboxes(function) + """
    <script>
    """


def maxwellian_graph(parameters):
    """
    maxwellian_graph(), plotting function responsible for the Maxwellian diagram.
    Parameters
    ----------
    parameters: Parameters in usage from the global parameters dict system.

    Returns
    -------
    A HTML string with embedded CSS and JS necessary to render a Maxwellian diagram,
    given values within 'parameters'.

    """
    # retrieves first both calculations and info values (illuminant E, purpleline)
    # specifically made into JSONs as the endpoints offer to make sure values given to plot
    # are not affected by floating point
    temp = parameters.copy()
    plots_json = cieapi.new_calculation_JSON(compute_Maxwellian_modular, temp)
    temp['info'] = True
    info_json = cieapi.new_calculation_JSON(compute_Maxwellian_modular, temp)
    # gets the points for the graph
    points = retrievePoints(maxwellian_graph, parameters)

    # creates formatted title, xaxis and yaxis names
    title = (
        "Maxwellian lm chromaticity diagram<br> Field size: {}°, "
        "Age: {} yr, Domain: {} nm - {} nm, Step: {} nm, Renormalized values".
        format(
            parameters['field_size'],
            parameters['age'],
            parameters['min'],
            parameters['max'],
            parameters['step_size']))
    xaxis = "l<sub> {}, {} ({}-{}, {})</sub>".format(
        parameters['field_size'],
        parameters['age'],
        parameters['min'],
        parameters['max'],
        parameters['step_size'])
    yaxis = "m<sub> {}, {} ({}-{}, {})</sub>".format(
        parameters['field_size'],
        parameters['age'],
        parameters['min'],
        parameters['max'],
        parameters['step_size'])

    # creates the html
    raw = head(maxwellian_graph) + """
    // converts JSONs from calculations to usable variables in JS
    const results = '""" + plots_json + """';
    const info = '""" + info_json + """';
    const plot = JSON.parse(results)['plot'];
    const information = JSON.parse(info);
    
    // creates generic layout and config for plotly
    const config = {responsive: true}
    var layout = {
        showlegend: false,
        autosize: true,
        title: '""" + title + """',
        margin: { l: 50, r: 10, b: 50, t: 50, pad: 4 },
        height: 800,
        width: 600,
                xaxis: {
                    nticks: 10,
                    zeroline: false,
                    title: '""" + xaxis + """',
                },
                yaxis: {
                    // attempted but failed attempt at 1:1 scale ratio
                    scaleanchor: "x",
                    scaleratio: 1,
                    zeroline: false,
                    title: '""" + yaxis + """'
                },
        }
    
    // from StackOverflow, see module description.
    output = plot[0].map((_, colIndex) => plot.map(row => row[colIndex]));
    
    // creates dictionary with values for maxwellian curve
    var curve = {
        x: output[1],
        y: output[2],
        mode: 'lines',
        line: {
                color: 'rgb(0, 0, 0)'
        }
    }
    
    // finds the positions on the curve where relevant points exist
    const y_points = []
    const x_points = []
    const pointes = """ + str(points) + """;
    for (let i = 0; i < pointes.length; i++) {
        let index = output[0].indexOf(pointes[i]);
        x_points.push(output[1][index]);
        y_points.push(output[2][index]);
    }
    
    // adds relevant points onto the curve with points
    var points = {
        x: x_points,
        y: y_points,
        mode: 'markers',
        type: 'scatter',
        textposition: 'top right',
        marker: {
            color: 'rgb(255, 255, 255)',
            size: 10,
            line: {
                color: 'rgb(0, 0, 0)',
                width: 2
            }
        }
    }
    
    // adds the illuminant E point
    var illuminantE = {
        x: [information['white'][0]],
        y: [information['white'][1]],
        mode: 'markers',
        type: 'scatter',
        textposition: 'top right',
        marker: {
            color: 'rgb(255, 255, 255)',
            size: 10,
            line: {
                color: 'rgb(0, 0, 0)',
                width: 2
            }
        }
    }
    
    // adds the purple stimulus line
    var purpleline = {
            x: [information['tg_purple'][0][1], information['tg_purple'][1][1]],
            y: [information['tg_purple'][0][2], information['tg_purple'][1][2]],
            mode: 'lines',
            line: {
                color: 'rgb(150, 32, 240)',
                width: 3
            }
        }
    
    // adds an event listener for the grid button to update the plotly function to use/not use grid
    grid.addEventListener('change', (event) => {
            var grid = document.getElementById('grid').checked;
            layout['yaxis']['showgrid'] = grid;
            layout['xaxis']['showgrid'] = grid;
            
            Plotly.react('plot', [curve, illuminantE, purpleline, points], layout, config);
    })
    
    // adds an event listener to label to update plotly function to either show or not the labels for points
    label.addEventListener('change', (event) => {
    var label = document.getElementById('label').checked;
            if (label) {
                points['mode'] = 'markers+text';
                points['text'] = """ + str(list(map(str, points))) + """;
                illuminantE['mode'] = 'markers+text';
                illuminantE['text'] = ['E'];
            } else {
                points['mode'] = 'markers';
                points['text'] = [];
                illuminantE['mode'] = 'markers';
                illuminantE['text'] = [];
            }
            Plotly.react('plot', [curve, illuminantE, purpleline, points], layout, config);
        })
    
    // uses a .react() to faster load the plot initially with intention of updating with .react() later
    Plotly.react('plot', [curve, illuminantE, purpleline, points], layout, config);
        </script>
    </body>
    </html>
    """
    return raw


def xyp_graph(parameters):
    """
    The plotting function for xy-p endpoint.

    Parameters
    ----------
    parameters: Parameters from global parameter system.

    Returns
    -------
    HTML representing the xy-p plot.

    """
    # finds both info and calculations for normal xy (to get curve) and info from xyz_purples
    temp = parameters.copy()
    temp['info'] = False
    # has to retrieve actual computation from xyz_purples for purpleline proper points
    purpleplot = compute_xyz_purples_modular(temp)['plot']
    xy_json = cieapi.new_calculation_JSON(compute_XY_modular, temp)
    temp['info'] = True
    info_json = cieapi.new_calculation_JSON(compute_xyz_purples_modular, temp)
    # creates formatted title
    title = ("xy cone-fundamental-based chromaticity diagram (purple-line stimuli)<br> Field size: {}°, Age: {} "
             "yr, Domain: {} nm - {} nm, Step: {} nm").format(
        parameters['field_size'],
        parameters['age'],
        parameters['min'],
        parameters['max'],
        parameters['step_size'])

    # creation of points, unlike previous ones which were ranges in essence,
    # needs exacts due to variations from parameters
    # based on plot.py in ciefunctions, lines 560, 575-578
    names = []
    points_x = []
    points_y = []
    points = np.arange(400, 700, 10)
    for l in points:
        ind = np.nonzero(purpleplot[:, 0] == l)[0]
        # creation of points from compute.py creates inhomogeneous array; filters them out
        if purpleplot[ind, 1]:
            names.append(l)
            points_x.append(purpleplot[ind, 1])
            points_y.append(purpleplot[ind, 2])
    purpleline = json.loads(info_json)['xyz_tg_purple']
    # formats them into strings to make them usable for embedded js
    names = '[' + str(purpleline[0][0]) + "," + ','.join(map(str, np.array(names).flatten())) + "," + str(
        purpleline[1][0]) + ']'
    points_x = '[' + str(purpleline[0][1]) + "," + ','.join(map(str, np.array(points_x).flatten())) + "," + str(
        purpleline[1][1]) + ']'
    points_y = '[' + str(purpleline[0][2]) + "," + ','.join(map(str, np.array(points_y).flatten())) + "," + str(
        purpleline[1][2]) + ']'

    # adds to title if normalization parameter is on
    if parameters['norm']:
        title += ", Renormalized values"

    # names xaxis and yaxis with formatting
    xaxis = "X<sub>F {}, {} ({}-{}, {})</sub>".format(
        parameters['field_size'],
        parameters['age'],
        parameters['min'],
        parameters['max'],
        parameters['step_size'])
    yaxis = "Y<sub>F {}, {} ({}-{}, {})</sub>".format(
        parameters['field_size'],
        parameters['age'],
        parameters['min'],
        parameters['max'],
        parameters['step_size'])

    raw = head(xyp_graph) + """
        // creates variables for values from JSONs in calculation
        const plot = JSON.parse('""" + cieapi.ndarray_to_JSON(
        purpleplot,
        ["{:.1f}", "{:.5f}", "{:.5f}", "{:.5f}"]) + """');
        const xy_plot = JSON.parse('""" + xy_json + """')['plot'];
        const info = JSON.parse('""" + info_json + """');
        
        // generic layout and config
        const config = {responsive: true}
        var layout = {
            showlegend: false,
            autosize: true,
            title: '""" + title + """',
            margin: { l: 50, r: 50, b: 50, t: 50, pad: 20},
            height: 800,
            width: 800,
                xaxis: {
                    nticks: 10,
                    zeroline: false,
                    title: '""" + xaxis + """',
                },
                yaxis: {
                    scaleanchor: "x",
                    zeroline: false,
                    title: '""" + yaxis + """'
                },
            }
        
        // from StackOverflow, see module description.
        output = plot[0].map((_, colIndex) => plot.map(row => row[colIndex]));
        output_xy = xy_plot[0].map((_, colIndex) => xy_plot.map(row => row[colIndex]));
        
        // creates the horseshoe curve for xy-p
        var curve = {
            x: output_xy[1],
            y: output_xy[2],
            xaxis: "xaxis",
            yaxis: "yaxis",
            mode: 'lines',
            line: {
                    color: 'rgb(0, 0, 0)'
            }
        }
        // creates an additional curve, purple coloured
        var curve2 = {
            x: output[1],
            y: output[2],
            xaxis: "xaxis",
            yaxis: "yaxis",
            mode: 'lines',
            line: {
                color: 'rgb(150, 32, 240)',
                width: 3
            }
        }
        
        // creates the relevant datapoints
        var points = {
            x: """ + points_x + """,
            y: """ + points_y + """,
            mode: 'markers',
            type: 'scatter',
            textposition: 'bottom right',
            marker: {
                color: 'rgb(255, 255, 255)',
                size: 10,
                line: {
                    color: 'rgb(0, 0, 0)',
                    width: 2
                }
            }
        }
        // creates the purple line
        var purpleline = {
            x: [info['xyz_tg_purple'][0][1], info['xyz_tg_purple'][1][1]],
            y: [info['xyz_tg_purple'][0][2], info['xyz_tg_purple'][1][2]],
            mode: 'lines',
            line: {
                color: 'rgb(150, 32, 240)',
                width: 3
            }
        }
        // creates the illuminant E point
        var illuminantE = {
            x: [info['xyz_white'][0]],
            y: [info['xyz_white'][1]],
            mode: 'markers',
            type: 'scatter',
            textposition: 'top right',
            marker: {
                color: 'rgb(255, 255, 255)',
                size: 10,
                line: {
                    color: 'rgb(0, 0, 0)',
                    width: 2
                    }
                }
        }
        
        render = [purpleline, curve, curve2, points, illuminantE]

        // event listener for grid
        grid.addEventListener('change', (event) => {
            var grid = document.getElementById('grid').checked;
            layout['yaxis']['showgrid'] = grid;
            layout['xaxis']['showgrid'] = grid;
            
            Plotly.react('plot', render, layout, config);
        })
        
        // eventlistener for the label button
        label.addEventListener('change', (event) => {
            var label = document.getElementById('label').checked;
            if (label) {
                points['mode'] = 'markers+text';
                points['text'] = """ + names + """;
                illuminantE['mode'] = 'markers+text';
                illuminantE['text'] = ['E'];
            } else {
                points['mode'] = 'markers';
                points['text'] = [];
                illuminantE['mode'] = 'markers';
                illuminantE['text'] = [];
            }
            Plotly.react('plot', render, layout, config);
        })
        
        Plotly.react('plot', render, layout, config);
    
        </script>
    </body>
</html>
    """

    return raw


def macleod_graph(parameters):
    """
    Plotting function for the MacLeod-Boynton diagram.
    Parameters
    ----------
    parameters: global parameter system in backend, given parameters from request.

    Returns
    -------
    HTML representing the Macleod-Boynton diagram given parameters.

    """
    # finds the plot and info for MacLeod to get both curve and purplelinestimulus+illuminant E
    temp = parameters.copy()
    plots_json = cieapi.new_calculation_JSON(compute_MacLeod_modular, temp)
    temp['info'] = True
    info_json = cieapi.new_calculation_JSON(compute_MacLeod_modular, temp)
    # retrieves relevant datapoints from a range
    points = retrievePoints(macleod_graph, parameters)

    # creates the formatted strings for title and xaxis/yaxis
    title = (
        "MacLeod-Boynton ls chromaticity diagram<br> Field size: {}°, Age: {} yr, Domain: {} nm - {} nm, Step: {} nm".
        format(parameters['field_size'], parameters['age'], parameters['min'], parameters['max'],
               parameters['step_size']))
    xaxis = "l<sub>MB</sub>. {}, {}".format(
        parameters['field_size'], parameters['age'])
    yaxis = "S<sub>MB</sub>. {}, {}".format(
        parameters['field_size'], parameters['age'])

    # creates the raw html
    raw = head(macleod_graph) + """
    // converts jsons from computation into variables within JS
    const results = '""" + plots_json + """';
    const info = '""" + info_json + """';
    const plot = JSON.parse(results)['plot'];
    const information = JSON.parse(info);
    
    // from StackOverflow, see module description.
    output = plot[0].map((_, colIndex) => plot.map(row => row[colIndex]));
    
    // generic config and layout
    const config = {responsive: true}
    var layout = {
        showlegend: false,
        autosize: true,
        title: '""" + title + """',
        margin: { l: 50, r: 10, b: 50, t: 50, pad: 4 },
        height: 800,
        width: 800,
            yaxis: {
                scaleanchor: "x",
                zeroline: false,
                title: '""" + yaxis + """'
            },
            xaxis: {
                zeroline: false,
                nticks: 10,
                title: '""" + xaxis + """',
            }
        }
    
    // macleod curve
    var curve = {
        x: output[1],
        y: output[3],
        xaxis: "x-aspect",
        yaxis: "y-aspect",
        mode: 'lines',
        line: {
                color: 'rgb(0, 0, 0)'
        }
    }
    
    // finds coordinate values for the datapoints within range,
    const y_points = []
    const x_points = []
    const pointes = """ + str(points) + """;
    for (let i = 0; i < pointes.length; i++) {
        let index = output[0].indexOf(pointes[i]);
        x_points.push(output[1][index]);
        y_points.push(output[3][index]);
    }
    
    // expresses the coordinate points from above into points for plot drawing
    var points = {
        x: x_points,
        y: y_points,
        mode: 'markers',
        type: 'scatter',
        textposition: 'top right',
        marker: {
            color: 'rgb(255, 255, 255)',
            size: 10,
            line: {
                color: 'rgb(0, 0, 0)',
                width: 2
            }
        }
    }
    // illuminant E point for Macleod
    var illuminantE = {
        x: [information['white'][0]],
        y: [information['white'][2]],
        mode: 'markers',
        type: 'scatter',
        textposition: 'top right',
        marker: {
            color: 'rgb(255, 255, 255)',
            size: 10,
            line: {
                color: 'rgb(0, 0, 0)',
                width: 2
            }
        }
    }
    // purple line stimulus for macleod
    var purpleline = {
        x: [information['tg_purple'][0][1], information['tg_purple'][1][1]],
        y: [information['tg_purple'][0][2], information['tg_purple'][1][2]],
        mode: 'lines',
        line: {
            color: 'rgb(150, 32, 240)',
            width: 3
        }
    }

    // adds event listeners for grid and label button as done earlier
    
    grid.addEventListener('change', (event) => {
        var grid = document.getElementById('grid').checked;
        layout['yaxis']['showgrid'] = grid;
        layout['xaxis']['showgrid'] = grid;
        
        Plotly.react('plot', [curve, points, illuminantE, purpleline], layout, config);
    })

    label.addEventListener('change', (event) => {
    var label = document.getElementById('label').checked;
        if (label) {
            points['mode'] = 'markers+text';
            points['text'] = """ + str(list(map(str, points))) + """;
            illuminantE['mode'] = 'markers+text';
            illuminantE['text'] = ['E'];
        } else {
            points['mode'] = 'markers';
            points['text'] = [];
            illuminantE['mode'] = 'markers';
            illuminantE['text'] = [];
        }
        Plotly.react('plot', [curve, points, illuminantE, purpleline], layout, config);
    })

    Plotly.react('plot', [curve, points, illuminantE, purpleline], layout, config);
    </script>
</body>
</html>
    """
    return raw


def XY_graph(parameters):
    """
    Plotting function for the 'xy' endpoint.
    Parameters
    ----------
    parameters: parameters for calculation, global system.

    Returns
    -------
    String representing HTML with plot and checkboxes.

    """
    # finds info and calculations for the xy endpoint function
    temp = parameters.copy()
    temp['info'] = False
    jsona = cieapi.new_calculation_JSON(compute_XY_modular, temp)
    temp['info'] = True
    info_json = cieapi.new_calculation_JSON(compute_XY_modular, temp)
    # retrieves relevant datapoints from range
    points = retrievePoints(XY_graph, parameters)

    # creates formatted strings representing title, xaxis and yaxis for plot
    title = ("CIE xy-cone fundamental-based chromaticity diagram<br>Field size: {}°, Age: {} yr, Domain: {} nm - "
             "{} nm, Step: {} nm").format(parameters['field_size'], parameters['age'], parameters['min'],
                                          parameters['max'], parameters['step_size'])
    if parameters['norm']:
        title += ", Renormalized values"
    xaxis = "X<sub>F{}, {} ({}-{}, {})</sub>".format(
        parameters['field_size'],
        parameters['age'],
        parameters['min'],
        parameters['max'],
        parameters['step_size'])
    yaxis = "Y<sub>F{}, {} ({}-{}, {})</sub>".format(
        parameters['field_size'],
        parameters['age'],
        parameters['min'],
        parameters['max'],
        parameters['step_size'])

    # constructs html for output
    raw = head(XY_graph) + """
    // converts calculations from JSON to variables within JS
    const plot = JSON.parse('""" + jsona + """')['plot'];
    const info = JSON.parse('""" + info_json + """');
    
    // generic layout/config
    const config = {responsive: true}
    var layout = {
        showlegend: false,
        autosize: true,
        title: '""" + title + """',
        margin: { l: 50, r: 10, b: 50, t: 50, pad: 4 },
        height: 800,
        width: 800,
            yaxis: {
                scaleanchor: "x",
                zeroline: false,
                title: '""" + yaxis + """'
            },
            xaxis: {
                zeroline: false,
                nticks: 10,
                title: '""" + xaxis + """',
            }
        }
    
    // from StackOverflow, see module description.
    output = plot[0].map((_, colIndex) => plot.map(row => row[colIndex]));
    
    // creates xy curve, horseshoe
    var curve = {
        x: output[1],
        y: output[2],
        mode: 'lines',
        line: {
                color: 'rgb(0, 0, 0)'
        }
    }
    
    // finds the relevant datapoints' values
    const y_points = []
    const x_points = []
    const pointes = """ + str(points) + """;
    for (let i = 0; i < pointes.length; i++) {
        let index = output[0].indexOf(pointes[i]);
        x_points.push(output[1][index]);
        y_points.push(output[2][index]);
    }
    // expresses them here
    var points = {
        x: x_points,
        y: y_points,
        mode: 'markers',
        type: 'scatter',
        textposition: 'top right',
        marker: {
            color: 'rgb(255, 255, 255)',
            size: 10,
            line: {
                color: 'rgb(0, 0, 0)',
                width: 2
            }
        }
    }
    
    // gets the illuminant E for xy
    var illuminantE = {
    x: [info['xyz_white'][0]],
    y: [info['xyz_white'][2]],
    mode: 'markers',
    type: 'scatter',
    textposition: 'top right',
    marker: {
        color: 'rgb(255, 255, 255)',
        size: 10,
        line: {
            color: 'rgb(0, 0, 0)',
            width: 2
        }
    }
}
    // gets purple line stimulus
    var purpleline = {
        x: [info['xyz_tg_purple'][0][1], info['xyz_tg_purple'][1][1]],
        y: [info['xyz_tg_purple'][0][2], info['xyz_tg_purple'][1][2]],
        mode: 'lines',
        line: {
            color: 'rgb(150, 32, 240)',
            width: 3
        }
    }
    
    // adds all of them to a list for easier tracking of below:
    var renders = [curve, points, illuminantE, purpleline]
    
    // adds constructions of xy_1931 and xy_1964 from functions, and corresponding event listeners
    
    """ + comparison_xy_1931(parameters) + """
    
    // event listener for cie1931,
    cie1931.addEventListener('change', (event) => {
        // if the checkbox for this is checked, then
        if (document.getElementById('cie1931').checked) {
        // var grid = document.getElementById('grid').checked;
            // add the variables from earlier construction into the "render" pile
            renders.push(curve_31, points_31, purpleline_31);
        } else {
            // if not, remove them
           renders = renders.filter( (element) => !( [curve_31, points_31, purpleline_31].includes(element)) );
        }
        // update graph
        Plotly.react('plot', renders, layout, config);
    })
    
    """ + comparison_xy_1964(parameters) + """
    
    cie1964.addEventListener('change', (event) => {
    // if checked,
        if (document.getElementById('cie1964').checked) {
        // var grid = document.getElementById('grid').checked;
        // push variables from construction of xy_1964 into render pile 
            renders.push(curve_64, points_64, purpleline_64);
        } else {
        // remove them if not ticked on
           renders = renders.filter( (element) => !( [curve_64, points_64, purpleline_64].includes(element)) );
        }
        // update plot to show it
        Plotly.react('plot', renders, layout, config);
    })
    
    // generic label event listener
    label.addEventListener('change', (event) => {
    var label = document.getElementById('label').checked;
        if (label) {
            points['mode'] = 'markers+text';
            points['text'] = """ + str(list(map(str, points))) + """;
            illuminantE['mode'] = 'markers+text';
            illuminantE['text'] = ['E'];
        } else {
            points['mode'] = 'markers';
            points['text'] = [];
            illuminantE['mode'] = 'markers';
            illuminantE['text'] = [];
        }
        Plotly.react('plot', renders, layout, config);
    })
    
    // generic grid event listener
    grid.addEventListener('change', (event) => {
        var grid = document.getElementById('grid').checked;
        layout['yaxis']['showgrid'] = grid;
        layout['xaxis']['showgrid'] = grid;
        
        Plotly.react('plot', renders, layout, config);
    })
    
    // initial creation of plot
    Plotly.react('plot', renders, layout, config);

        </script>
    </body>
</html>
    """
    return raw


def XYZP_graph(parameters):
    """
    Plotting function for the xyz-p endpoint.
    Parameters
    ----------
    parameters

    Returns
    -------

    """
    # finds only the calculations (info either not needed or not existing)
    temp = parameters.copy()
    data = cieapi.new_calculation_JSON(compute_XYZ_purples_modular, temp)
    # creates formatted title
    title = ("XYZ cone-fundamental-based tristumulus functions for purple-line stimuli<br>Field size: "
             "{}°, Age: {} yr, Domain: {} nm - {} nm, Step: {} nm").format(
        parameters['field_size'],
        parameters['age'],
        parameters['min'],
        parameters['max'],
        parameters['step_size'])

    if parameters['norm']:
        title += ", Renormalized values"

    # creates the html for output
    raw = head(XYZP_graph) + """
        // parses calculation into variable through json
        const xyzp = JSON.parse('""" + data + """')['plot'];
        
        // from StackOverflow, see module description.
        const output = xyzp[0].map((_, colIndex) => xyzp.map(row => row[colIndex]));
        
        
        // uses transposed output above to interpret into x, y, z curves with colours
        var r = {
            x: output[0],
            y: output[1],
            mode: 'lines',
            name: 'x',
            line: {
            color: 'rgb(255, 0, 0)'
            }
        }
        var g = {
            x: output[0],
            y: output[2],
            mode: 'lines',
            name: 'y',
            line: {
            color: 'rgb(0, 127, 0)'
            }
        }
        var b = {
            x: output[0],
            y: output[3],
            mode: 'lines',
            name: 'z',
            line: {
            color: 'rgb(0, 0, 255)'
            }
        }
        
        // generic config/layout
        const config = {responsive: true}
        var layout = {
            showlegend: false,
            title: '""" + title + """',
            autosize: true,
            height: 700,
                yaxis: {
                    zeroline: false,
                    automargin: true,
                    title: "Cone-fundamental-based tristumulus values",
                },
                xaxis: {
                    automargin: true,
                    title: "Complementary wavelength (nm)"
                }
            }
        
        renders = [r, g, b]
        // adds event listener for grid checkbox
        grid.addEventListener('change', (event) => {
            var grid = document.getElementById('grid').checked;
            layout['yaxis']['showgrid'] = grid;
            layout['xaxis']['showgrid'] = grid;
            // updates
            Plotly.react('plot', renders, layout, config);
        })
        // initial creation of plot
        Plotly.react('plot', renders, layout, config);
        </script>
    </body>
</html>
    """
    return raw


def comparison_xy_1964(parameters, mode="dot"):
    """
    Plotting function for the xy-1964 (field_size 10) standard function, both endpoint
    and for comparison checkboxes in other endpoints. Specifically made to be put into other HTML outputs.
    Parameters
    ----------
    parameters: parameters from global system
    mode: string representing the render mode for the plot, either solid (for standard function endpoint)
    or empty/"dot" for comparisons in other endpoints.

    Returns
    -------
    String representing partial-created HTML.

    """
    # finds both calculations and info
    temp = parameters.copy()
    temp['field_size'] = 10
    temp['info'] = False
    data = cieapi.new_calculation_JSON(compute_xyz_standard_modular, temp)
    temp['info'] = True
    info_data = cieapi.new_calculation_JSON(compute_xyz_standard_modular, temp)
    # finds relevant datapoints
    points = retrievePoints(XY_graph, parameters)

    # returns partially constructed html
    return """
    // parses calculations from computation into variables for JS.
    const cie_1964 = JSON.parse('""" + data + """')['plot'];
    const info1964 = JSON.parse('""" + info_data + """');
    // from StackOverflow, see module description.
    const output3 = cie_1964[0].map((_, colIndex) => cie_1964.map(row => row[colIndex]));

    // makes a curve for the standard function here
    var curve_64 = {
        x: output3[1],
        y: output3[2],
        mode: 'lines',
        line: {
            dash: '""" + mode + """',
            color: 'rgb(0, 0, 0)'
        }
    }
    
    // finds relevant datapoints, and makes into variable for plotting.
    const y_points_1964 = []
    const x_points_1964 = []
    const pointes_1964 = """ + str(points) + """;
    for (let i = 0; i < pointes_1964.length; i++) {
        let index = output3[0].indexOf(pointes_1964[i]);
        x_points_1964.push(output3[1][index]);
        y_points_1964.push(output3[2][index]);
    }
    var points_64 = {
        x: x_points_1964 ,
        y: y_points_1964,
        mode: 'markers',
        type: 'scatter',
        textposition: 'top right',
        marker: {
            color: 'rgb(125, 125, 125)',
            size: 10,
            line: {
                color: 'rgb(0, 0, 0)',
                width: 2
            }
        }
    }
    // finds the purpleline for standardization function
    var purpleline_64 = {
        x: [info1964['tg_purple'][0][1], info1964['tg_purple'][1][1]],
        y: [info1964['tg_purple'][0][2], info1964['tg_purple'][1][2]],
        mode: 'lines',
        line: {
            dash: '""" + mode + """',
            color: 'rgb(150, 32, 240)',
            width: 3
        }
    }

    """


def comparison_xy_1931(parameters, mode="dash"):
    """
    Partial-HTML constructor for plotting of xy-1931 (field size 2).
    Parameters
    ----------
    parameters: parameters from global system
    mode: string representing the render mode for the plot, either solid (for standard function endpoint), or "dash"
    for when in usage for other endpoints for comparison.

    Returns
    -------
    Partially constructed HTML with values from computation.
    """

    # finds relevant info and calculations,
    temp = parameters.copy()
    temp['field_size'] = 2
    temp['info'] = False
    data = cieapi.new_calculation_JSON(
        compute_xyz_standard_modular,
        temp)
    temp['info'] = True
    info_data = cieapi.new_calculation_JSON(
        compute_xyz_standard_modular,
        temp)
    # retrieves relevant datapoints
    points = retrievePoints(XY_graph, parameters)

    # returns html
    return """
    // makes the variables from calculation into js variables
    const cie_1931 = JSON.parse('""" + data + """')['plot'];
    const info1931 = JSON.parse('""" + info_data + """');
    // from StackOverflow, see module description.
    const output2 = cie_1931[0].map((_, colIndex) => cie_1931.map(row => row[colIndex]));
    
    // makes curve into variable
    var curve_31 = {
        x: output2[1],
        y: output2[2],
        mode: 'lines',
        line: {
            dash: '""" + mode + """',
            color: 'rgb(0, 0, 0)'
        }
    }
    
    // makes points into variable after finding them
    const y_points_1931 = []
    const x_points_1931 = []
    const pointes_1931 = """ + str(points) + """;
    for (let i = 0; i < pointes_1931.length; i++) {
        let index = output2[0].indexOf(pointes_1931[i]);
        x_points_1931.push(output2[1][index]);
        y_points_1931.push(output2[2][index]);
    }
    var points_31 = {
        x: x_points_1931 ,
        y: y_points_1931,
        mode: 'markers',
        type: 'scatter',
        textposition: 'top right',
        marker: {
            color: 'rgb(0, 0, 0)',
            size: 10,
            line: {
                color: 'rgb(0, 0, 0)',
                width: 2
            }
        }
    }
    
    // finds purpleline and expresses as variable
    var purpleline_31 = {
        x: [info1931['tg_purple'][0][1], info1931['tg_purple'][1][1]],
        y: [info1931['tg_purple'][0][2], info1931['tg_purple'][1][2]],
        mode: 'lines',
        line: {
            dash: '""" + mode + """',
            color: 'rgb(150, 32, 240)',
            width: 3
        }
    }
    
    """


def XYZ_graph(parameters):
    """
    Plotting function for the xyz endpoint.
    Parameters
    ----------
    parameters: parameters from global system

    Returns
    -------
    Fully constructed string within HTML for the plotting of xyz endpoint.

    """
    # finds the calculation, not info due to not needed or non existant
    json = cieapi.new_calculation_JSON(compute_XYZ_modular, parameters)
    # creates formatted string title
    title = (
        "CIE XYZ cone-fundamental-based tristumulus functions<br>Field size: {}°"
        ", Age: {} yr, Domain: {} nm - {} nm, Step: {} nm".
        format(parameters['field_size'], parameters['age'], parameters['min'], parameters['max'],
               parameters['step_size']))
    # adds it to the title
    if parameters['norm']:
        title += ", Renormalized values"

    # generates the html
    raw = head(XYZ_graph) + """
        // makes into js variables from original computation
        const json = '""" + json + """';
        const plot = JSON.parse(json)['plot'];
        // from StackOverflow, see module description.
        const output = plot[0].map((_, colIndex) => plot.map(row => row[colIndex]));
        
        // finds the three tristumuluses xyz from transposed output
        var r = {
            x: output[0],
            y: output[1],
            mode: 'lines',
            name: 'x',
            line: {
                color: 'rgb(255, 0, 0)'
            }
        }
        var g = {
            x: output[0],
            y: output[2],
            mode: 'lines',
            name: 'y',
            line: {
                color: 'rgb(0, 127, 0)'
            }
        }
        var b = {
            x: output[0],
            y: output[3],
            mode: 'lines',
            name: 'z',
            line: {
                color: 'rgb(0, 0, 255)'
            }
        }
        
        // generic config/layout for plotly
        const config = {responsive: true}
        var layout = {
            showlegend: false,
            title: '""" + title + """',
            autosize: true,
            height: 700,
                yaxis: {
                    zeroline: false,
                    automargin: true,
                    title: "Cone-fundamental-based tristumulus values",
                },
                xaxis: {
                    automargin: true,
                    title: "Wavelength (nm)"
                }
            }
            
        renders = [r, g, b]
        
        // adds partially constructed htmls for comparison graphs xyz 1931 and xyz 1964
        
        """ + comparsion_graph_1931(parameters) + """
        
        // adds event listener for xyz 1931
        cie1931.addEventListener('change', (event) => {
            if (document.getElementById('cie1931').checked) {
            // var grid = document.getElementById('grid').checked;
                renders.push(cr, cg, cb);
            } else {
               renders = renders.filter( (element) => !( [cr, cg, cb].includes(element)) );
            }
            console.log(renders);
            Plotly.react('plot', renders, layout, config);
        })
        
        """ + comparsion_graph_1964(parameters) + """
        
        // adds event listener for xyz 1964 checkbutton
        cie1964.addEventListener('change', (event) => {
            if (document.getElementById('cie1964').checked) {
                renders.push(cr_64, cg_64, cb_64);
            } else {
               renders = renders.filter( (element) => !( [cr_64, cg_64, cb_64].includes(element)) );
            }
            Plotly.react('plot', renders, layout, config);
        })
        
        // event listener for grid checkbox
        grid.addEventListener('change', (event) => {
            var grid = document.getElementById('grid').checked;
            layout['yaxis']['showgrid'] = grid;
            layout['xaxis']['showgrid'] = grid;
            
            Plotly.react('plot', renders, layout, config);
        })
        
        // initial creation of plot
        Plotly.react('plot', renders, layout, config);
        </script>
    </body>
</html>
    
    """
    return raw


def comparsion_graph_1931(parameters, mode="dot"):
    """
    Plotting function for xyz 1931 (field size 2), with different mode of render depending on
    if by itself or for comparisons.
    Parameters
    ----------
    parameters: parameters from global system
    mode: String that is either "lines" for when function plots by itself (standardization endpoint),
    or empty/"dot" when used in another function for comparison.

    Returns
    -------
    Partially constructed HTML within a string for the parts of xyz 1931.
    """
    # finds the calculations necessary
    temp = parameters.copy()
    temp['field_size'] = 2
    data = cieapi.new_calculation_JSON(compute_XYZ_standard_modular, temp)
    # constructs the string of html
    raw = """
        // makes calculation data into variable
        const data = '""" + data + """';
        const comp_1931 = JSON.parse(data)['plot'];
        // from StackOverflow, see module description.
        const output_1931 = comp_1931[0].map((_, colIndex) => comp_1931.map(row => row[colIndex]));
        
        // expresses the cie xyz 1931 as cr, cg and cb variables for plotly
        var cr = {
            x: output_1931[0],
            y: output_1931[1],
            mode: 'lines',
            name: 'x',
            line: {
                dash: '""" + mode + """',
                color: 'rgb(255, 0, 0)'
            }
        }
        var cg = {
            x: output_1931[0],
            y: output_1931[2],
            mode: 'lines',
            name: 'y',
            line: {
                dash: '""" + mode + """',
                color: 'rgb(0, 127, 0)'
            }
        }
        var cb = {
            x: output_1931[0],
            y: output_1931[3],
            mode: 'lines',
            name: 'z',
            line: {
                dash: '""" + mode + """',
                color: 'rgb(0, 0, 255)'
            }
        }
        
    """
    return raw


def cieXYZ_std(parameters):
    """
    Plotting function for xyz-std endpoint.
    Parameters
    ----------
    parameters: parameters from the global system

    Returns
    -------
    Constructed HTML for xyz-std plot within a string.

    """
    # has to first route depending on the field_size;
    if parameters['field_size'] == 2:
        # decides the 'type' for checkboxes; cie1931 needs cie1964 as a checkbox,
        # while cie1964 needs cie1931 as one
        type = "cie1931_2"
        # decides the modes for both functions, how they get drawn
        mode1931 = "solid"
        mode1964 = "dot"
        # the starter variables for plotly to render
        starter = "[cr, cb, cg]"
        # different titles as well
        title = "CIE 1931 XYZ standard 2° colour-matching functions"
    else:
        type = "cie1964_10"
        mode1931 = "dot"
        mode1964 = "solid"
        starter = "[cr_64, cg_64, cb_64]"
        title = "CIE 1964 XYZ standard 10° colour-matching functions"

    # creates the html
    raw = head(type) + """
    
    // adds the variables for comparison
    """ + comparsion_graph_1931(parameters, mode1931) + comparsion_graph_1964(parameters, mode1964) + """
    
    // adds generic config/layout for plotly
    const config = {responsive: true}
    var layout = {
        showlegend: false,
        title: '""" + title + """',
        autosize: true,
        height: 700,
            yaxis: {
                zeroline: false,
                automargin: true,
                title: "Tristumulus values",
            },
            xaxis: {
                automargin: true,
                title: "Wavelength (nm)"
            }
        }
    
    // makes a render pile of what to render in plotly
    renders = """ + starter + """;
    
    // adds event listeners for both regardless of disabled or enabled; users wont be able
    // to get them regardless
    cie1931.addEventListener('change', (event) => {
        if (document.getElementById('cie1931').checked) {
        var grid = document.getElementById('grid').checked;
            renders.push(cr, cg, cb);
        } else {
           renders = renders.filter( (element) => !( [cr, cg, cb].includes(element)) );
        }
        console.log(renders);
        Plotly.react('plot', renders, layout, config);
    })
    
    cie1964.addEventListener('change', (event) => {
        if (document.getElementById('cie1964').checked) {
            renders.push(cr_64, cg_64, cb_64);
        } else {
           renders = renders.filter( (element) => !( [cr_64, cg_64, cb_64].includes(element)) );
        }
        Plotly.react('plot', renders, layout, config);
    })
    
    // generic eventlistener for grid
    grid.addEventListener('change', (event) => {
        var grid = document.getElementById('grid').checked;
        layout['yaxis']['showgrid'] = grid;
        layout['xaxis']['showgrid'] = grid;
        
        Plotly.react('plot', renders, layout, config);
    })
    
    // initial drawing of plot
    Plotly.react('plot', renders, layout, config);

        </script>
    </body>
</html>
        
    """
    return raw


def ciexyz_std(parameters):
    """
    Plotting function for the xy-std endpoint.
    Parameters
    ----------
    parameters: parameters from the global system

    Returns
    -------
    String with constructed HTML for xy-std plots.
    """
    # routes it much like cieXYZ_std(),
    if parameters['field_size'] == 2:
        type = "xyz1931_2"
        mode1931 = "solid"
        mode1964 = "dot"
        starter = "[curve_31, points_31, purpleline_31, illuminantE]"
        title = "CIE 1931 xy standard 2° chromaticity diagram"
        main = "points_31"
    else:
        type = "xyz1964_10"
        mode1931 = "dot"
        mode1964 = "solid"
        starter = "[curve_64, points_64, purpleline_64, illuminantE]"
        title = "CIE 1964 xy standard 10° chromaticity diagram"
        main = "points_64"

    # creates html
    raw = head(type) + """
    // adds the values/variables from comparison functions
    """ + comparison_xy_1931(parameters, mode1931) + comparison_xy_1964(parameters, mode1964) + """
    
    // generic config/layout
    const config = {responsive: true}
    var layout = {
        showlegend: false,
        title: '""" + title + """',
        autosize: false,
        height: 800,
        width: 800,
            yaxis: {
                zeroline: false,
                scaleanchor: "xaxis",
                automargin: true,
                title: '""" + "y<sub>{}</sub>".format(parameters['field_size']) + """',
            },
            xaxis: {
                automargin: true,
                nticks: 10,
                domain: "contraint",
                title: '""" + "x<sub>{}</sub>".format(parameters['field_size']) + """',
            }
        }
    
    // illuminantE point
    var illuminantE = {
        x: [info1931['white'][0]],
        y: [info1931['white'][1]],
        mode: 'markers',
        type: 'scatter',
        textposition: 'top right',
        marker: {
            color: 'rgb(255, 255, 255)',
            size: 10,
            line: {
                color: 'rgb(0, 0, 0)',
                width: 2
            }
        }
    
    }
    
    renders = """ + starter + """;
    
    // adds generic event listeners for both, cannot be used if enabled so it's fine to add both
    cie1931.addEventListener('change', (event) => {
        if (document.getElementById('cie1931').checked) {
        var grid = document.getElementById('grid').checked;
            renders.push(curve_31, points_31, purpleline_31);
        } else {
           renders = renders.filter( (element) => !( [curve_31, points_31, purpleline_31].includes(element)) );
        }
        console.log(renders);
        Plotly.react('plot', renders, layout, config);
    })
    
    cie1964.addEventListener('change', (event) => {
        if (document.getElementById('cie1964').checked) {
            renders.push(curve_64, points_64, purpleline_64);
        } else {
           renders = renders.filter( (element) => !( [curve_64, points_64, purpleline_64].includes(element)) );
        }
        Plotly.react('plot', renders, layout, config);
    })
    
    // label checkbox event listener
    label.addEventListener('change', (event) => {
    var label = document.getElementById('label').checked;
        if (label) {
            """ + main + """['mode'] = 'markers+text';
            """ + main + """['text'] = pointes_1931;
            illuminantE['mode'] = 'markers+text';
            illuminantE['text'] = ['E'];
        } else {
            """ + main + """['mode'] = 'markers';
            """ + main + """['text'] = [];
            illuminantE['mode'] = 'markers';
            illuminantE['text'] = [];
        }
        Plotly.react('plot', renders, layout, config);
    })
    
    // grid event listener 
    grid.addEventListener('change', (event) => {
        var grid = document.getElementById('grid').checked;
        layout['yaxis']['showgrid'] = grid;
        layout['xaxis']['showgrid'] = grid;
        
        Plotly.react('plot', renders, layout, config);
    })
    
    // initial creation of plot
    Plotly.react('plot', renders, layout, config);

        </script>
    </body>
</html>
    
    
    """
    return raw


def comparsion_graph_1964(parameters, mode="dash"):
    """
    Partial constructor for xyz-1964 (field size 10) plot.
    Parameters
    ----------
    parameters: parameters from global system
    mode: String representing either normal plotting (value of "lines") or when used in comparison
    (value of none/"dash")

    Returns
    -------
    Partial construction of HTML for xyz-1964 in plot as string.

    """
    # calculated the XYZ with field size of 10 for computations
    temp = parameters.copy()
    temp['field_size'] = 10
    data = cieapi.new_calculation_JSON(compute_XYZ_standard_modular, temp)
    raw = """
        // converts calculation from python to js variables through js
        const data2 = '""" + data + """';
        const comp_1964 = JSON.parse(data2)['plot'];
        // from StackOverflow, see module description.
        const output_1964 = comp_1964[0].map((_, colIndex) => comp_1964.map(row => row[colIndex]));

        // creates three curves representing the xyz from standardization function
        var cr_64 = {
            x: output_1964[0],
            y: output_1964[1],
            mode: 'lines',
            name: 'x',
            line: {
                dash: '""" + mode + """',
                color: 'rgb(255, 0, 0)'
            }
        }
        var cg_64 = {
            x: output_1964[0],
            y: output_1964[2],
            mode: 'lines',
            name: 'y',
            line: {
                dash: '""" + mode + """',
                color: 'rgb(0, 127, 0)'
            }
        }
        var cb_64 = {
            x: output_1964[0],
            y: output_1964[3],
            mode: 'lines',
            name: 'z',
            line: {
                dash: '""" + mode + """',
                color: 'rgb(0, 0, 255)'
            }
        }

    """
    return raw


def LMS_graph(parameters):
    """
    The plotting function for the LMS endpoint.
    Parameters
    ----------
    parameters: parameters from global system

    Returns
    -------
    Completely constructed HTML for LMS plot.

    """
    # generate computations for LMS + log LMS
    json = cieapi.new_calculation_JSON(compute_LMS_modular, parameters)
    temp = parameters.copy()
    temp['log'] = not parameters['log']
    other_json = cieapi.new_calculation_JSON(compute_LMS_modular, temp)

    # creates title customary of given log and base
    titles = ["CIE 2006 LMS cone fundamentals",
              "<br> Field size: {}°, Age: {} yr, Domain: {} nm - {} nm, Step: {} nm",
              "<br> Field size: {}°, Age: {} yr, Domain: {} nm - {} nm, Step: {} nm, Logarithmic values"]
    if parameters['base']:
        titles[0] += " (9 signs. figs. data)"

    title = titles[0] + titles[1].format(parameters['field_size'], parameters['age'], parameters['min'],
                                         parameters['max'], parameters['step_size'])
    log_title = titles[0] + titles[2].format(parameters['field_size'], parameters['age'], parameters['min'],
                                             parameters['max'], parameters['step_size'])

    # adds functionality to tackle specifically given
    if parameters['log']:
        startervariant = "true"
    else:
        startervariant = "false"

    # creates the html with head() and embedded js code
    raw = head(LMS_graph) + """
        // finds checkbox for logarithmic value enabling,
        // shifts it on or off depending on optionals in url
        const checkbox = document.querySelector("#log");
        checkbox.checked = """ + startervariant + """
    
        // creates variables from jsonified calculations for both normal and log lms
        const json = '""" + json + """';
        var one = JSON.parse(json);
        const loga = '""" + other_json + """';
        var log = JSON.parse(loga);
        
        // creates variables for their plots
        const plot = one['plot'];
        const log_plot = log['plot'];
        
        // from StackOverflow, see module description.
        output = plot[0].map((_, colIndex) => plot.map(row => row[colIndex]));
        output2 = log_plot[0].map((_, colIndex) => log_plot.map(row => row[colIndex]));
        // above, transposes them
        
        // creates them into variables for plotly to be used
        var test = {
            name: 'S',
            x: output[0],
            y: output[3],
            mode: 'lines',
            line: {
                color: 'rgb(0, 0, 255)'
            }
        }
        var test2 = {
            name: 'M',
            x: output[0],
            y: output[2],
            mode: 'lines',
            line: {
                color: 'rgb(0, 127, 0)'
            }
        }
        var test3 = {
            name: 'L',
            x: output[0],
            y: output[1],
            mode: 'lines',
            line: {
                color: 'rgb(255, 0, 0)'
            }
        }
        var test4 = {
            name: 'S',
            x: output2[0],
            y: output2[3],
            mode: 'lines',
            line: {
                color: 'rgb(0, 0, 255)'
            }
        }
        var test5 = {
            name: 'M',
            x: output2[0],
            y: output2[2],
            mode: 'lines',
            line: {
                color: 'rgb(0, 127, 0)'
            }
        }
        var test6 = {
            name: 'L',
            x: output2[0],
            y: output2[1],
            mode: 'lines',
            line: {
                color: 'rgb(255, 0, 0)'
            }
        }
        
        // generic config/layout system for plotly
        const config = {responsive: true}
        var layout = {
            showlegend: false,
            autosize: true,
            height: 700,
                yaxis: {
                    zeroline: false,
                    automargin: true,
                },
                xaxis: {
                    automargin: true,
                }
            }
            
        // adds event listener for grid
        grid.addEventListener('change', (event) => {
            var grid = document.getElementById('grid').checked;
            layout['yaxis']['showgrid'] = grid;
            layout['xaxis']['showgrid'] = grid;
            
            var event = new Event('change');
            checkbox.dispatchEvent(event);
        })
        
        // adds unique listener for logarithmic checkbox
        checkbox.addEventListener('change', (event) => {
          if (event.currentTarget.checked) {
            layout['yaxis']['title'] = "Log10 (relative energy sensitivity)"
            layout['xaxis']['title'] = "Wavelength (nm)"
            layout['title'] = '""" + log_title + """'
            var newa = [test4, test5, test6];
            Plotly.react('plot', newa, layout, config);
          } else {
            layout['yaxis']['title'] = "Relative energy sensitivities"
            layout['xaxis']['title'] = "Wavelength (nm)"
            layout['title'] = '""" + title + """';
            var newa = [test, test2, test3];
            Plotly.react('plot', newa, layout, config);
          }
        })
        
        // instead of previous functions, starts the initial drawing by dispatching a change event
        // to the checkbox, forcing it to essentially react and draw either a log or normal lms
        var event = new Event('change');
        checkbox.dispatchEvent(event);
    </script>
</body>
</html>
"""
    return raw
