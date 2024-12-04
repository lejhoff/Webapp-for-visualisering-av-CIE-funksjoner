#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cieapi: Webserver application for backend for server.

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

import math
import json
import time
from sanic import Sanic, response, SanicException
from sanic.response import json, html
from sanic_cors import CORS
from sanic.exceptions import NotFound

from computemodularization import compute_LMS_modular, compute_xyz_purples_modular, compute_XYZ_standard_modular
from descriptionapi import *
from graph import LMS_graph, macleod_graph, maxwellian_graph, XYZ_graph, XY_graph, XYZP_graph, xyp_graph, \
    cieXYZ_std, ciexyz_std
from compute import chop


api = Sanic(__name__)
CORS(api, resources={r"/*": {"origins": "*"}})

# constants for each endpoint
API_HOMEPAGE = "/api"
API_VERSION = "v2"
LMS_ENDPOINT = "lms"
LMS_MB_ENDPOINT = "lms-mb"
LMS_MW_ENDPOINT = "lms-mw"
XYZ_ENDPOINT = "xyz"
XY_ENDPOINT = "xy"
XYZP_ENDPOINT = "xyz-p"
XYP_ENDPOINT = "xy-p"
XYZSTD_ENDPOINT = "xyz-std"
XYSTD_ENDPOINT = "xy-std"
STATUS_ENDPOINT = "status"
# constants for standardization field sizes
STD_1931 = 2.0
STD_1964 = 10.0

# Timer that starts when server boots up, for status endpoint
server_start = time.time()


# bad practice, but valid for us now
@api.middleware("request")
async def check_get(request):
    """
    Bad practice, but valid for us.
    A middleware function that checks the method of the request; if it is not GET, then raise an exception
    and return an error response.

    All of our endpoints only support GET, and will seemingly so for the future. However, if this service gets
    expanded on in the future to support several HTTP Methods, then this middleware has to go.
    """
    if request.method != "GET":
        raise SanicException(
            ("METHOD ERROR",
             "The HTTP Method you are trying to use is not supported by any endpoint in this server.",
             "All of the endpoints support only HTTP GET requests. We suggest you try that instead."),
            status_code=405)


@api.exception(NotFound)
async def notfound_handler(request, exception):
    return json(
        {
            "error": "Not Found",
            "status_code": 404,
            "message": "Path you are trying to visit does not exist.",
            "suggestion": "Please try another page, such as '/'."
        }, status=404
    )


@api.exception(SanicException)
async def error_handler(request, exception):
    """
    SanicException error handler function that returns a JSON with information regarding the exception.

    Parameters
    ----------
    request: Unusued but customary parameter for the request itself.
    exception: Parameter symbolizing the request.

    Returns
    -------
    A HTML response with a JSON containing the title of the error, a message detailing it, a possible suggestion
    for the user to do, and the status code itself.

    """
    [title, message, suggestion] = exception.args[0]
    json_error = {
        "error": title,
        "status_code": exception.status_code,
        "message": message,
        "suggestion:": suggestion,
    }
    return json(json_error, status=exception.status_code)


def endpoint_creator(homepage, version, endpoint=""):
    """
    Helper function that creates the endpoints based on the constants described above.
    Parameters
    ----------
    homepage: Constant for the API homepage.
    version: Constant for the API version.
    endpoint: The constant for a wished endpoint.

    Returns
    -------
    The combined URL.

    """
    return '/'.join([homepage, version, endpoint])


"""
    A constant for the calculation formats. The new method that this server uses requires specific
    string formats for specific endpoints, so this is used to control that. 
    For example, the first value of LMS-base-log's result is a ":.1f", which symbolizes a float with one decimal.
    This means that every first value of every row in the calculation of LMS-base-log will be printed
    into the JSON string as a float with one decimal.
"""
calculation_formats = {
    "LMS-base-log": {
        "result": ["{:.1f}", "{:.8f}", "{:.8f}", "{:.8f}"],
        "plot": ["{:.1f}", "{:.8f}", "{:.8f}", "{:.8f}"],
    },
    "LMS-base": {
        "result": ["{:.1f}", "{:.8e}", "{:.8e}", "{:.8e}"],
        "plot": ["{:.1f}", "{:.8e}", "{:.8e}", "{:.8e}"],
    },
    "LMS-log": {
        "result": ["{:.1f}", "{:.5f}", "{:.5f}", "{:.5f}"],
        "plot": ["{:.1f}", "{:.5f}", "{:.5f}", "{:.5f}"],
    },
    "LMS": {
        "result": ["{:.1f}", "{:.5e}", "{:.5e}", "{:.5e}"],
        "plot": ["{:.1f}", "{:.5e}", "{:.5e}", "{:.5e}"],
    },
    "Maxwell-Macleod-resplot": {
        "result": ["{:.1f}", "{:.6f}", "{:.6f}", "{:.6f}"],
        "plot": ["{:.1f}", "{:.6f}", "{:.6f}", "{:.6f}"],
    },
    "XYZ-XYZP-XYZ-STD": {
        "result": ["{:.1f}", "{:.6e}", "{:.6e}", "{:.6e}"],
        "plot": ["{:.1f}", "{:.6e}", "{:.6e}", "{:.6e}"],
    },
    "XY-XYP-XY-STD": {
        "result": ["{:.1f}", "{:.5f}", "{:.5f}", "{:.5f}"],
        "plot": ["{:.1f}", "{:.5f}", "{:.5f}", "{:.5f}"],
    },
    # shared dictionary between all info
    "info-1": {
        "norm": ["{:.8f}", "{:.8f}", "{:.8f}"],
        "white": ["{:.6f}", "{:.6f}", "{:.6f}"],
        # "white_plot": ["{:.6f}", "{:.6f}", "{:.6f}"],
        "tg_purple": ["{:.6f}", "{:.6f}", "{:.6f}"],
        # "tg_purple_plot": ["{:.6f}", "{:.6f}", "{:.6f}"],
        "xyz_white": ["{:.5f}", "{:.5f}", "{:.5f}"],
        "xyz_tg_purple": ["{:.5f}", "{:.5f}", "{:.5f}"],
        "XYZ_tg_purple": ["{:.5f}", "{:.5f}", "{:.5f}", "{:.5f}"],
        "trans_mat": ["{:.8f}", "{:.8f}", "{:.8f}"],
        # "trans_mat_N": ["{:.8f}", "{:.8f}", "{:.8f}"],
    }
}

# static file hosting
api.static("/", "./templates/index.html", name="home-page")
api.static("/api/v2/", "./templates/api-page.html", name="api-page")


def new_calculation_JSON(calculation, parameters):
    """
    A routing-like function that routes to a correct format from calculation_formats, based on
    the calculation and format. Different calculations have different needs for string formats, and the
    same goes for parameters. This makes sure the right one is used for each endpoint.

    Parameters
    ----------
    calculation: The calculation function from computemodularization.py.
    parameters: A dictionary of treated URL parameters.

    Returns
    -------
    A raw JSON string representing the output data from the computational function, given the parameters.

    """
    if parameters['info']:
        return write_to_JSON(calculation(parameters), calculation_formats['info-1'])

    if calculation is compute_LMS_modular:
        if parameters['base']:
            if parameters['log']:
                # log10 base LMS
                return write_to_JSON(calculation(parameters), calculation_formats['LMS-base-log'])
            else:
                # base LMS
                return write_to_JSON(calculation(parameters), calculation_formats['LMS-base'])
        else:
            # log10 LMS
            if parameters['log']:
                return write_to_JSON(calculation(parameters), calculation_formats['LMS-log'])
            else:
                # LMS
                return write_to_JSON(calculation(parameters), calculation_formats['LMS'])
    # many of these share the same ones
    if calculation in [compute_Maxwellian_modular, compute_MacLeod_modular]:
        return write_to_JSON(calculation(parameters), calculation_formats["Maxwell-Macleod-resplot"])
    if calculation in [compute_XYZ_modular, compute_XYZ_purples_modular, compute_XYZ_standard_modular]:
        return write_to_JSON(calculation(parameters), calculation_formats["XYZ-XYZP-XYZ-STD"])
    else:
        return write_to_JSON(calculation(parameters), calculation_formats["XY-XYP-XY-STD"])


def write_to_JSON(results_dict, json_dict):
    """
    A function that takes in a dictionary of results, as well as a dictionary of expected formats.
    The function will take the results dictionary, and format it as a map container in JSON string with
    special formats to values of results given the formats in json_dict.

    Parameters
    ----------
    results_dict: A dictionary of the results from a calculation endpoint.
    json_dict: A dictionary retrieved from the constant dictionary declared globally.

    Returns
    -------
    A JSON string that depicts a map container with the same values as results_dict, just formatted as
    json_dict wishes.

    """
    something = {}
    for (name, body) in results_dict.items():
        something[name] = ndarray_to_JSON(body, json_dict[name])
    output = []
    for (name, body) in something.items():
        temp = '"{}":'.format(name) + body
        output.append(temp)
    fin = ','.join(output)
    return '{' + fin + '}'


def ndarray_to_JSON(body, formatta):
    """
    A function that takes in a ndarray and an expected "format" (array of format strings), to then
    reconvert it into a JSON String of the array. Unlike json.dumps() and other functions like that,
    it will format each member of the ndarray as specificed by the "format" - but this is given
    that the length of the current row in the ndarray is as long/equal shape as the format.

    Parameters
    ----------
    body: A ndarray symbolizing something to be converted into a JSON string.
    formatta: An array symbolizing the format each row in 'body' should be formatted as.

    Returns
    -------
    A JSON string of the ndarray, with the formats specified.

    """
    # for later consideration; have it return a value that is not dict nor array
    # if (not isinstance(body, dict)) and (not isinstance(body, numpy.ndarray)):
    # not necessary for our needs now, but perhaps for later

    # If the current 'body' is an 1D array (which either happens because of parameter being originally
    # an 1D-array, or by an ndarray recursively calling this function for each row)...
    if body.ndim == 1:
        # Double check if the length of the row is equal to the length of the format
        if len(body) == len(formatta):
            # Format each row respectively as they should be, through indexed for-loop:
            all = []
            for index in range(len(body)):
                # Retrieve the format and chopped body.
                tempar = chop(body[index])
                asda = formatta[index]
                # The '-inf' produced by LMS (log10) is something that cannot be parsed by JSON;
                # it gets remade into null instead.
                if math.isinf(body[index]):
                    tempar = "null"
                    asda = "{}"
                # Append the formatted string to the 'all' array, symbolizing 'all' elements of current row.
                all.append(asda.format(tempar))
            # Join them all with commas, and then output it with [ ] on either side, succesfully making it into
            # a JSON array.
            output = ','.join(all)
            return '[' + output + ']'
        else:
            # should only happen if the row format of a calculation does not match
            # the given format (example, [x, y, z] =/= [f1, f2]
            raise SanicException(
                ("PROCESSING ERROR",
                 "There has been an error inside of the server.",
                 "Contact system administrator for server, or try again later."),
                status_code=500)
    else:
        # create empty array
        temp = []
        # for each array in current array, recursively call to each and append them to array above
        for row in body:
            temp.append(ndarray_to_JSON(row, formatta))
        # join them with commas, and output with [ ]
        output = ','.join(temp)
        return '[' + output + ']'

# handler for old version
@api.get("/api/v1")
async def old_version(request):
    """
    Handler of old version of API.
    """
    raise SanicException(("NOT SUPPORTED", "API v1 is not supported anymore.",
                          "Please use the newest version of the API available ({}).".format(API_VERSION)),
                         status_code=501)

"""
    The endpoints for the API.     
    They are all very equal, so all meaningful comments go here.
    
    They all have four paths/routes:
        - /calculation, which sends a raw response of a JSON string with content_type of application/json
        - /sidfemenu, returns a generated HTML of a sidemenu given the function and parameters
        - /plot, returns a generated HTML of a diagram/plot for the function with parameters
        - /{}, anything else it returns an error message of 404 with message
"""


def not_found(more):
    """
    Helper function that reduces repeats in endpoints below while still giving
    a meaningful error message.
    """
    raise SanicException(("NOT FOUND", "Invalid value ({}) for route.".format(more),
                          "Please ensure that the value of your route is supported. "
                          "The supported endpoints are: 'calculation', 'sidemenu' or 'plot'."),
                         status_code=404)

# lms


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, LMS_ENDPOINT) + "/<more:str>")
async def lms(request, more: str):
    if more == "calculation":
        return response.raw(new_calculation_JSON(compute_LMS_modular,
                                                 create_and_check_parameters(
                                                     True,
                                                     compute_LMS_modular,
                                                     request)),
                            content_type="application/json",
                            headers={"cache-control": "private"})
    if more == "sidemenu":
        return html(LMS_sidemenu(create_and_check_parameters(
            True,
            compute_LMS_modular,
            request)),
            headers={"cache-control": "private"})
    if more == "plot":
        return html(LMS_graph(create_and_check_parameters(
            True,
            compute_LMS_modular,
            request)),
            headers={"cache-control": "private"})
    else:
        not_found(more)


# macleod
@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, LMS_MB_ENDPOINT) + "/<more:str>")
async def macleod(request, more: str):
    if more == "calculation":
        return response.raw(new_calculation_JSON(compute_MacLeod_modular,
                                                 create_and_check_parameters(
                                                     True,
                                                     compute_MacLeod_modular,
                                                     request)),
                            content_type="application/json",
                            headers={"cache-control": "private"})
    if more == "sidemenu":
        return html(LMS_MB_sidemenu(create_and_check_parameters(
            True,
            compute_MacLeod_modular,
            request)),
            headers={"cache-control": "private"})
    if more == "plot":
        return html(macleod_graph(create_and_check_parameters(
            True,
            compute_MacLeod_modular,
            request)),
            headers={"cache-control": "private"})
    else:
        not_found(more)


# maxwellian
@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, LMS_MW_ENDPOINT) + "/<more:str>")
async def maxwellian(request, more: str):
    if more == "calculation":
        return response.raw(new_calculation_JSON(compute_Maxwellian_modular,
                                                 create_and_check_parameters(
                                                     True,
                                                     compute_Maxwellian_modular,
                                                     request)),
                            content_type="application/json",
                            headers={"cache-control": "private"})
    if more == "sidemenu":
        return html(LMS_MW_sidemenu(create_and_check_parameters(
            True,
            compute_Maxwellian_modular,
            request)),
            headers={"cache-control": "private"})
    if more == "plot":
        return html(maxwellian_graph(create_and_check_parameters(
            True,
            compute_Maxwellian_modular,
            request)),
            headers={"cache-control": "private"})
    else:
        not_found(more)


# xyz
@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, XYZ_ENDPOINT) + "/<more:str>")
async def xyz(request, more: str):
    if more == "calculation":
        return response.raw(new_calculation_JSON(compute_XYZ_modular,
                                                 create_and_check_parameters(
                                                     True,
                                                     compute_XYZ_modular,
                                                     request)),
                            content_type="application/json",
                            headers={"cache-control": "private"})
    if more == "sidemenu":
        return html(XYZ_sidemenu(create_and_check_parameters(
            True,
            compute_XYZ_modular,
            request)),
            headers={"cache-control": "private"})
    if more == "plot":
        return html(XYZ_graph(create_and_check_parameters(
            True,
            compute_XYZ_modular,
            request)),
            headers={"cache-control": "private"})
    else:
        not_found(more)

# xy


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, XY_ENDPOINT) + "/<more:str>")
async def xy(request, more: str):
    if more == "calculation":
        return response.raw(
            new_calculation_JSON(compute_XY_modular,
                                 create_and_check_parameters(
                                     True,
                                     compute_XY_modular,
                                     request)),
            content_type="application/json",
            headers={"cache-control": "private"})
    if more == "sidemenu":
        return html(XY_sidemenu(create_and_check_parameters(
            True,
            compute_XY_modular,
            request)),
            headers={"cache-control": "private"})
    if more == "plot":
        return html(XY_graph(create_and_check_parameters(
            True,
            compute_XY_modular,
            request)),
            headers={"cache-control": "private"})
    else:
        not_found(more)


# xyz purples
@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, XYZP_ENDPOINT) + "/<more:str>")
async def xyz_p(request, more: str):
    if more == "calculation":
        return response.raw(
            new_calculation_JSON(compute_XYZ_purples_modular,
                                 create_and_check_parameters(
                                     True,
                                     compute_XYZ_purples_modular,
                                     request)),
            content_type="application/json",
            headers={"cache-control": "private"})
    if more == "sidemenu":
        return html(XYZP_sidemenu(create_and_check_parameters(
            True,
            compute_XYZ_purples_modular,
            request)),
            headers={"cache-control": "private"})
    if more == "plot":
        return html(XYZP_graph(create_and_check_parameters(
            True,
            compute_XYZ_purples_modular,
            request)),
            headers={"cache-control": "private"})
    else:
        not_found(more)


# xy purples
@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, XYP_ENDPOINT) + "/<more:str>")
async def xy_p(request, more: str):
    if more == "calculation":
        return response.raw(
            new_calculation_JSON(compute_xyz_purples_modular,
                                 create_and_check_parameters(
                                     True,
                                     compute_xyz_purples_modular,
                                     request)),
            content_type="application/json",
            headers={"cache-control": "private"})
    if more == "sidemenu":
        return html(XYP_sidemenu(create_and_check_parameters(
            True,
            compute_xyz_purples_modular,
            request)),
            headers={"cache-control": "private"})
    if more == "plot":
        return html(xyp_graph(create_and_check_parameters(
            True,
            compute_xyz_purples_modular,
            request)),
            headers={"cache-control": "private"})
    else:
        not_found(more)


# xyz standardization
@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, XYZSTD_ENDPOINT) + "/<more:str>")
async def xyz_std(request, more: str):
    if more == "calculation":
        return response.raw(
            new_calculation_JSON(compute_XYZ_standard_modular,
                                 create_and_check_parameters(
                                     False,
                                     compute_XYZ_standard_modular,
                                     request)),
            content_type="application/json",
            headers={"cache-control": "private"})
    if more == "sidemenu":
        return html(XYZ_std_sidemenu(create_and_check_parameters(
            False,
            compute_XYZ_standard_modular,
            request)),
            headers={"cache-control": "private"})
    if more == "plot":
        return html(cieXYZ_std(create_and_check_parameters(
            False,
            compute_XYZ_standard_modular,
            request)),
            headers={"cache-control": "private"})
    else:
        not_found(more)

# xy standardization


@api.get(endpoint_creator(API_HOMEPAGE, API_VERSION, XYSTD_ENDPOINT) + "/<more:str>")
async def xy_std(request, more: str):
    if more == "calculation":
        return response.raw(
            new_calculation_JSON(compute_xyz_standard_modular,
                                 create_and_check_parameters(
                                     False,
                                     compute_xyz_standard_modular,
                                     request)),
            content_type="application/json",
            headers={"cache-control": "private"})
    if more == "sidemenu":
        return html(XY_std_sidemenu(create_and_check_parameters(
            False,
            compute_xyz_standard_modular,
            request)),
            headers={"cache-control": "private"})
    if more == "plot":
        return html(ciexyz_std(create_and_check_parameters(
            False,
            compute_xyz_standard_modular,
            request)),
            headers={"cache-control": "private"})
    else:
        not_found(more)


@api.route(endpoint_creator(API_HOMEPAGE, API_VERSION, STATUS_ENDPOINT), methods=["GET"])
def status_endpoint(request):
    """
    A simple endpoint that returns a status, the current uptime of the server in seconds, and the current
    version of the API.
    """
    status = {
        "status": 200,
        "uptime": str(time.time() - server_start) + "s",
        "version": API_VERSION
    }
    return response.json(status, status=200, headers={"cache-control": "no-store"})


def create_and_check_parameters(disabled, calculation, request):
    """
    'create_and_check_parameters(...)' is a function that takes in three parameters described below, to then
    either return a dictionary containing the processed URL parameters - or stop abruptely due to a raise of
    SanicException in case of an error.

    Parameters
    ----------
    disabled: A boolean which changes treatment of parameters if it is on or not; used to distinguish between
    standardization functions and the other ones - as standardization functions require only 'field_size', while
    the other ones require also 'age' at least.
    calculation: The calculation function used, to make error handling for specific functions possible (for example,
    it shouldn't be possible to pass the "log" parameter to something that is not the "/lms" endpoint.
    request: The Sanic request object, containing arguments.

    Returns
    -------
    A dictionary that contains the parsed and treated URL parameters, or won't finish due to raised exception
    caused by error handling.

    """

    # error handling
    def string_to_type_else(string, given_type, other):
        # try to make the string into an instance of type
        try:
            return given_type(string)
        # if it cannot be converted to type, then return the "other"
        except ValueError:
            return other
        # however, if there is a typerror (such as passing None to float()), then return None
        except TypeError:
            return None

    # for all functions except standardization functions:
    if disabled:
        # uses checkArgument to fill in all mandatory parameters
        parameters = {
            # mostly mandatory parameters
            "field_size": string_to_type_else(request.args.get('field_size'), float, None),
            "age": string_to_type_else(request.args.get('age'), float, None)
        }

        # checks if mandatory parameters are present
        for (name, value) in parameters.items():
            if value is None:
                raise SanicException(
                    ("VALUE ERROR", "Invalid input for '{}' either due to absence or invalid type".format(name),
                     "Control that '{}' is present, and is of the 'float' type.".format(name)), status_code=422)

        parameters['age'] = round(parameters['age'])

        # sees if optional parameters present, makes them default to their usual values in the case they are
        # not present
        optionals = {
            # are either None (if arg is not present at all),
            # a float value if the arg is present and is a float,
            # or a -1 if the arg is present, but not float
            "min": string_to_type_else(request.args.get('min'), float, -1),
            "max": string_to_type_else(request.args.get('max'), float, -1),
            "step_size": string_to_type_else(request.args.get('step_size'), float, -1),
        }

        for (name, value) in optionals.items():
            # if not correct type
            if value is -1:
                raise SanicException((
                    "TYPE ERROR",
                    "Invalid input for '{}' due to invalid type".format(name),
                    "Control that the value is of a 'float' type, or remove it to use default settings."),
                    status_code=422)
            # if not present at all
            if value is None:
                given = 0
                if name == "min":
                    given = 390.0
                if name == "max":
                    given = 830.0
                if name == "step_size":
                    given = 1.0
                parameters.update({name: given})
            # if present and correct type
            else:
                parameters.update({name: float(value)})

        # error handling for the values
        if parameters['field_size'] > 10 or parameters['field_size'] < 1:
            raise SanicException(("VALUE ERROR", "Invalid value for 'field_size'.",
                                  "Control that the value is between 1.0 and 10.0."), status_code=422)
        if parameters['age'] < 20 or parameters['age'] > 80:
            raise SanicException(("VALUE ERROR", "Invalid value for 'age'",
                                  "Control that the value is between 20.0 and 80.0."), status_code=422)
        if parameters['min'] < 390 or parameters['min'] > 400:
            raise SanicException(("VALUE ERROR", "Invalid value for 'min'-imum domain.",
                                  "Control that the value is between 390.0 and 400.0. "
                                  "Alternatively, remove it from URL."),
                                 status_code=422)
        if parameters['max'] > 830 or parameters['max'] < 700:
            raise SanicException(("VALUE ERROR", "Invalid value for 'max'-imum domain.",
                                  "Control that the value is between 700.0 and 830.0."), status_code=422)
        if parameters['step_size'] > 5 or parameters['step_size'] < 0.1:
            raise SanicException(("VALUE ERROR", "Invalid value for 'step size'",
                                  "Control that the value is between 0.1 and 5.0."), status_code=422)

        # ----------------------

        optionals = {
            'log': False,
            'base': False,
            'info': False,
            'norm': False,
            'sidemenu': False,
        }

        # if there is anything with "optional" in URL
        if request.args.get('optional') is not None:
            # split it by the comma to make a list of entries
            params = request.args.get('optional').split(',')
            # for every element in this list, see if it exists in the optional parameter dictionary keys; if it does,
            # then make that key's body True
            for param in params:
                if param in optionals.keys():
                    optionals[param] = True
                else:
                    raise SanicException(
                        ("VALUE ERROR", "Parameter list 'optional' contains unknown parameter '{}'.".format(param),
                         "Check if the parameter has correct value, and try again. Alternatively, remove it if not."),
                        status_code=422)

        if optionals['sidemenu'] and optionals['info']:
            raise SanicException(("Value error", "Cannot combine parameters 'sidemenu' and 'info'.",
                                  "Please remove one of them from the URL."), 422)

        for (name, body) in optionals.items():
            if body:
                if (name == "log" or name == "base") and (calculation is not compute_LMS_modular):
                    raise SanicException(("Value error",
                                          "Invalid usage of '{}' for endpoint.".format(
                                              name),
                                          "The '{}' parameter is exclusive to the /lms endpoint. "
                                          "Please remove it from the URL.".format(name)),
                                         status_code=422)
                if (((name == "info") and (calculation is compute_LMS_modular))
                        or ((name == "norm") and (calculation in [compute_LMS_modular, compute_MacLeod_modular,
                                                                  compute_Maxwellian_modular]))):
                    raise SanicException(("Value error",
                                          "Invalid usage of '{}' for endpoint.".format(
                                              name),
                                          "This endpoint does not support {}. Please, verify this, and try again. "
                                          "If not, remove it from URL.".format(name)),
                                         status_code=422)
            parameters.update({
                name: body
            })

        # parameter that cannot be triggered by any URL parameter,
        # exclusive to XYZ-purples in usage for compute_xy_modular
        # in order to save time
        parameters['purple'] = False
        # std-xy needs xyz-std, saves time
        parameters['xyz-std'] = False

        return parameters

    else:
        parameters = {"field_size": string_to_type_else(
            request.args.get('field_size'), float, None)}
        if parameters['field_size'] is None:
            raise SanicException(("Value error", "The value of 'field_size' is not present.",
                                 "Please make sure that the parameter is present as "
                                  "a float value that is either 2.0 or 10.0."),
                                 status_code=422)

        optionals = {
            'log': False,
            'base': False,
            'info': False,
            'norm': False
        }
        #                 if name == "min": given = 390.0
        #                 if name == "max": given = 830.0
        #                 if name == "step_size": given = 1.0
        parameters['min'] = 390.0
        parameters['max'] = 830.0
        parameters['step_size'] = 1.0

        # if there is anything with "optional" in URL
        if request.args.get('optional') is not None:
            # split it by the comma to make a list of entries
            params = request.args.get('optional').split(',')
            # for every element in this list, see if it exists in the optional parameter dictionary keys; if it does,
            # then make that key's body True
            for param in params:
                if param in optionals.keys():
                    optionals[param] = True
                else:
                    raise SanicException(
                        (
                            "VALUE ERROR",
                            "Parameter list 'optional' contains unknown parameter '{}'.".format(
                                param),
                            "Check if the parameter has correct value, and try again. "
                            "Alternatively, remove it if not."),
                        status_code=422)
            # else, if it is not in it, then throw error

        for (name, body) in optionals.items():
            if body is None:
                if body is None:
                    parameters.update({name: False})
                    continue
            if body:
                if name == "log" or name == "base":
                    raise SanicException(("Value error", "Invalid usage of '{}' for endpoint.".format(name),
                                          "The '{}' parameter is exclusive to the /lms endpoint. "
                                          " remove it from the URL.".format(
                                              name)), status_code=422)
                if ((name == "info") and (calculation is compute_XYZ_standard_modular)) or (name == "norm"):
                    raise SanicException(("Value error", "Invalid usage of '{}' for endpoint.".format(name),
                                          "This endpoint does not support {}. Please, verify this, and try again. "
                                          "If not, remove it from URL.".format(
                                              name)), status_code=422)
            parameters.update({
                name: body
            })

        if parameters['field_size'] == STD_1931 or parameters['field_size'] == STD_1964:
            return parameters

        raise SanicException(("Value error", "Invalid value for 'field_size'.",
                              "Please make sure that the parameter is present as a float "
                              "value that is either 2.0 or 10.0."),
                             status_code=422)


if __name__ == '__main__':
    api.run(host="0.0.0.0", port=8000, workers=4)
