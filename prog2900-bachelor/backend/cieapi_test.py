#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
cieapi_test: Testing module for cieapi.py and endpoints.

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

import json
import pytest
import numpy as np
import pandas as pd
import cieapi as cieapi


def json_lint_test(json_string):
    """
    The program has to format JSON strings to get the correct values for each calculation, so to ensure
    that our JSONs are valid, this is a function that tries to load them. If it fails, returns False - else, returns
    True.

    Parameters
    ----------
    json_string: JSON String that one would like to test.

    Returns
    -------
    A boolean that is either True if the json_string is indeed a valid JSON String, or False if it is not.

    """
    try:
        json.loads(json_string)
    except ValueError:
        return False
    return True


# simple test case for ndarray_to_JSON
def test_ndarray_to_JSON():
    """
    Testing the 'ndarray_to_JSON()' function from cieapi.py. Testing a simple case of a one dimensional array,
    both checking if it is the value it should be *and* if the value is JSON lintable.
    The function in question should format the given array based on the format given, and return the array
    as a JSON string of the array with the formats applied to the respective elements of the array.

    Returns
    -------
    Nothing, just asserts if the array is allike the expected string, and if it is JSON lintable.

    """
    format = ['{:.3f}', '{:.3f}', '{:.3f}', '{:.3f}']
    basic = np.array([1.0, 2.0, 3.0, 4.0])
    assert "[1.000,2.000,3.000,4.000]" == cieapi.ndarray_to_JSON(basic, format)
    assert json_lint_test(cieapi.ndarray_to_JSON(basic, format)) is True


# advanced and realistic case
def test_advanced_ndarray_to_JSON():
    """
    An advanced test of 'ndarray_to_JSON()' function from cieapi.py, tests with a ndarray.

    Returns
    -------
    The JSON string of a ndarray with the formatted elements being as they should.

    """
    advanced = np.array([[0.8934598, 0.87234879, 123.3453, 1239.234],
                         [0.3982475, 0.8438345, 253.00, 2545.4385],
                         [0.234854, 0.348589, 7554.45, 9523.4755]])
    format = ['{:.7f}', '{:.7f}', '{:.5e}', '{:.5e}']
    answer = ("[[0.8934598,0.8723488,1.23345e+02,1.23923e+03],"
              "[0.3982475,0.8438345,2.53000e+02,2.54544e+03],"
              "[0.2348540,0.3485890,7.55445e+03,9.52348e+03]]")
    assert answer == cieapi.ndarray_to_JSON(advanced, format)
    assert json_lint_test(cieapi.ndarray_to_JSON(advanced, format)) is True


# testing writing a dict with ndarrays to JSON
def test_write_to_JSON():
    """
    The 'test_write_to_JSON()' function tests the 'write_to_JSON()' from cieapi.py, by using the functions tested
    above inside of a dictionary - to then return the dictionary as a JSON String with the arrays formatted as
    wished.

    Returns
    -------
    Nothing, just asserts if the produced JSON String is of the expected value, and sees if it is lintable.

    """
    format = {
        "example": ["{:.3f}", "{:.3f}", "{:.3f}", "{:.3f}"],
    }
    case = {
        "example": np.array([
            [234.1248, 1232.3874, 0.00245, 0.43533],
            [754.1234, 0.35475, 0.00245, 0.43533],
            [9595.243, 4573.324, 1.1111, 45345.232]
        ])
    }
    answer = ('{"example":[[234.125,1232.387,0.002,0.435],'
              '[754.123,0.355,0.002,0.435],'
              '[9595.243,4573.324,1.111,45345.232]]}')
    assert answer == cieapi.write_to_JSON(case, format)
    assert json_lint_test(cieapi.write_to_JSON(case, format)) is True


# testing the endpoint creator function to see if it creates correct URLs
def test_endpoint_creator():
    assert "/home/v10/testingendpoint" == cieapi.endpoint_creator(
        "/home", "v10", "testingendpoint")


"""
    A series of endpoint tests. Because the endpoints are asynchronous, the testing module was changed to
    accodomate for the 'pytest' module, alongside 'pytest-asyncio'.
"""


@pytest.mark.asyncio
async def test_home_endpoint():
    """
        Performs a GET request to the main page, and asserts the value if it is 200 (Successful).
    """
    req, response = await cieapi.api.asgi_client.get("/")
    assert response.status == 200


@pytest.mark.asyncio
async def test_wrong_endpoint():
    """
        Performs a GET request to a nonexisting page, and asserts the value if it is 404 (Not Found).
    """
    req, response = await cieapi.api.asgi_client.get("/asdasdasd")
    assert response.status == 404


@pytest.mark.asyncio
async def test_api_endpoint():
    """
        Performs a GET request to the API homepage, and asserts the value if it is 200 (Successful).
    """
    req, response = await cieapi.api.asgi_client.get("/api/v2/")
    assert response.status == 200


def load_csv_to_array(file_path):
    """
    'load_csv_to_array()' is a helper function that just reads in a given csv file as a np ndarray,
    only used for parsing in the csv files made from the software for comparison testing with results
    from endpoints.

    Parameters
    ----------
    file_path: A string symbolizing the filepath + file of a CSV file one wishes to read.

    Returns
    -------

    """
    return pd.read_csv(file_path, header=None).to_numpy()


# tests lms endpoint
@pytest.mark.asyncio
async def test_lms_endpoint():
    """
        Performs a GET request to the /lms endpoint, and compares result with corresponding csv file
        produced from the CIE Functions software.
    """
    truth_data = load_csv_to_array("./tests/LMS-1-25-1.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/lms/calculation?field_size=1&age=25")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200


# tests macleod endpoint
@pytest.mark.asyncio
async def test_lmsmb_endpoint():
    """
        Performs a GET request to the /lms-mb endpoint, and compares result with corresponding csv file
        produced from the CIE Functions software.
    """
    truth_data = load_csv_to_array("./tests/LMS-MB-5-63-1.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/lms-mb/calculation?field_size=5&age=63")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200


# tests maxwellian endpoint
@pytest.mark.asyncio
async def test_lmsmw_endpoint():
    """
        Performs a GET request to the /lms-w endpoint, and compares result with corresponding csv file
        produced from the CIE Functions software.
    """
    truth_data = load_csv_to_array("./tests/LMS-MW-45-45-1.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/lms-mw/calculation?field_size=4.5&age=45")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200


# tests XYZ endpoint
@pytest.mark.asyncio
async def test_xyz_endpoint():
    """
        Performs a GET request to the /xyz endpoint, and compares result with corresponding csv file
        produced from the CIE Functions software.
    """
    truth_data = load_csv_to_array("./tests/XYZ-38-52-15.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/xyz/calculation?field_size=3.8&age=52&step_size=1.5")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200


# tests XY endpoint

@pytest.mark.asyncio
async def test_xy_endpoint():
    """
        Performs a GET request to the /xy endpoint, and compares result with corresponding csv file
        produced from the CIE Functions software.
    """
    truth_data = load_csv_to_array("./tests/XY-31-71-1.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/xy/calculation?field_size=3.1&age=71")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200


# tests xy-purple endpoint,
@pytest.mark.asyncio
async def test_xyp_endpoint():
    """
        Performs a GET request to the /xyp endpoint, and compares result with corresponding csv file
        produced from the CIE Functions software.
        There is no testing of the /xyzp endpoint, as the software crashes when producing a table from it.
    """
    truth_data = load_csv_to_array("./tests/XYP-20-32-1.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/xy-p/calculation?field_size=2&age=32")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200


# testing standardization function for xyz
@pytest.mark.asyncio
async def test_xyzstd_endpoint():
    """
        Performs a GET request to the /xyz-std endpoint, and compares result with corresponding csv file
        produced from the CIE Functions software.
    """
    truth_data = load_csv_to_array("./tests/XYZ-STD-2.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/xyz-std/calculation?field_size=2")
    assert np.all(np.array(json.loads(response.body)['result']) == truth_data) == True
    assert response.status == 200


# testing standardization function for xy
@pytest.mark.asyncio
async def test_xystd_endpoint():
    """
        Performs a GET request to the /xy-std endpoint, and compares result with corresponding csv file
        produced from the CIE Functions software.
    """
    truth_data = load_csv_to_array("./tests/XY-STD-2.csv")
    req, response = await cieapi.api.asgi_client.get("/api/v2/xy-std/calculation?field_size=2")
    assert np.all(np.array(json.loads(response.body)['plot']) == truth_data) == True
    assert response.status == 200


# testing various parameters

"""
    The following functions merely test the different parameters, seperately in their own functions as to not
    disturb each other in their asynchronicity.
"""


@pytest.mark.asyncio
async def test_param1_endpoint():
    test_case = ('{"norm":[0.6993641,0.34253216,0.03040997],"white":[0.71312,0.28688,0.016007],"tg_purple":[[409.5,'
                 '0.663468,0.951054],[699.9,0.969648,0]]}')
    req, response = await cieapi.api.asgi_client.get("/api/v2/lms-mb/calculation"
                                                     "?field_size=1.5&age=51&max=700&optional=info")
    assert json.loads(response.body) == json.loads(test_case)


@pytest.mark.asyncio
async def test_param2_endpoint():
    test_case = ('{"white":[0.333300,0.333330,0.333370],"tg_purple":[[360.200000,0.182210,0.019980],'
                 '[700.900000,0.720360,0.279640]]}')
    req, response = await cieapi.api.asgi_client.get("/api/v2/xy-std/calculation?field_size=10.0&optional=info")
    assert json.loads(response.body) == json.loads(test_case)


@pytest.mark.asyncio
async def test_param3_endpoint():
    test_case = ('{"xyz_white":[0.33333,0.33333,0.33333],"xyz_tg_purple":[[409.70000,0.16304,0.01656],[703.30000,'
                 '0.72329,0.27671]],"XYZ_tg_purple":[[409.70000,0.08657,0.00879,0.43561],[703.30000,0.00863,0.00330,'
                 '0.00000]]}')
    req, response = await cieapi.api.asgi_client.get("/api/v2/xy-p/calculation?field_size=2&age=32&optional=info")
    assert json.loads(response.body) == json.loads(test_case)


@pytest.mark.asyncio
async def test_param4_endpoint():
    test_case = ('{"trans_mat":[[1.93122240,-1.42718225,0.40529507],[0.68367008,0.35153487,0.00000000],[0.00000000,'
                 '0.00000000,1.94811216]]}')
    req, response = await cieapi.api.asgi_client.get("/api/v2/xyz-p/calculation?field_size=2.0&age=20&optional=info")
    assert json.loads(response.body) == json.loads(test_case)
