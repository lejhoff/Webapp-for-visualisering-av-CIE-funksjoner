#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
descriptionapi: Module consisting of functions responsible for generating HTML pages as
                they are within the CIE Functions application.

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
    NOTE:
    
    This module contains code based on the description.py module for CIE Functions:
    https://github.com/ifarup/ciefunctions/blob/master/tc1_97/description.py

    It contains both the direct usage of functions, as well as functions based on ones
    that exist in that module.
"""


# ------------------------------------------------------------------------------------------

"""
    A version of _head() based on the one in description.py without included MathJax as file.
    description.py, lines 25-61
"""

import sys

import cieapi
import styles.description
from computemodularization import compute_MacLeod_modular, compute_Maxwellian_modular, compute_XYZ_modular, \
    compute_XY_modular, compute_XYZ_purples_modular, compute_xyz_standard_modular


def _head():
    html_string = """
    <head>
        <style>  
            body {
            font-family: Sans-Serif;
            }
            .matrix {
                position: relative;
                border-spacing: 10px 0;
            }
            .matrix:before {
                content: "";
                position: absolute;
                left: -6px;
                top: 0;
                border: 1px solid #000;
                border-right: 0px;
                width: 6px;
                height: 100%;
            }
            .matrix:after {
                content: "";
                position: absolute;
                right: -6px;
                top: 0;
                border: 1px solid #000;
                border-left: 0px;
                width: 6px;
                height: 100%;
            }
        </style>
    <script type="text/javascript"
    src="http://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
    </script>
    <script type="text/x-mathjax-config">
        MathJax.Hub.Config({
            displayAlign: "left",
            showProcessingMessages: false,
            messageStyle: "none",
            inlineMath:[["\\(","\\)"]],
            displayMath:[["$$","$$"]],
            tex2jax: { preview: "none" },
            "HTML-CSS": {
    """
    if sys.platform.startswith('win'):
        html_string += """
                scale: 95
        """
    elif sys.platform.startswith('linux'):
        html_string += """
                scale: 95
        """
    else:
        html_string += """
                scale: 100
        """
    html_string += """
            }
        });
    </script>
    </head> 
    """
    return html_string


"""
    The following functions are identical to their counterparts in description.py,
    just without the "_sidemenu" suffix. These have been adjusted to use the 'parameters' dictionary system
    that the entire program is revolved around, but remain mostly - if not almost near identical to their
    original counterparts.
"""


def LMS_sidemenu(parameters):
    """
    LMS_sidemenu(...) is directly based on LMS(...) from description.py, lines 1089-1122.

    Parameters
    ----------
    parameters: Global parameter system, dict of user inputs.

    Returns
    -------
    Generated HTML page with sidemenu contents.

    """
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    params = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    params['λ_min'] = params['min']
    params['λ_max'] = params['max']
    params['λ_step'] = params['step_size']
    params['log10'] = params['log']

    if parameters['base']:
        html_string += styles.description._heading(
            'CIE LMS cone fundamentals (9 sign. figs.)')
    else:
        html_string += styles.description._heading('CIE LMS cone fundamentals')
    html_string += (
        styles.description._parameters(params) +
        styles.description._functions('\\(\\bar l_{%s,\,%d}\\)' %
                                      (params['field_size'],
                                       params['age']),
                                      '\\(\\bar m_{\,%s,\,%d}\\)' %
                                      (params['field_size'],
                                       params['age']),
                                      '\\(\\bar s_{%s,\,%d}\\)' %
                                      (params['field_size'],
                                       params['age']),
                                      '\\(\\lambda\\) &nbsp;(wavelength)') +
        styles.description._wavelenghts(params) +
        styles.description._normalization_LMS(params) +
        styles.description._precision_LMS(params, params['base'])
    )
    return html_string


def LMS_MB_sidemenu(parameters):
    """
    LMS_MB_sidemenu(...) is based directly on description.py, lines 1161-1196.

    Parameters
    ----------
    parameters: Global parameter system, dict of user inputs.

    Returns
    -------
    Generated HTML page with sidemenu contents.

    """
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['λ_min'] = data['min']
    data['λ_max'] = data['max']
    data['λ_step'] = data['step_size']

    # needs info from macleod, does computation
    data['info'] = True
    info = compute_MacLeod_modular(data)
    data['norm_coeffs_lms_mb'] = info['norm']
    data['lms_mb_white'] = info['white']
    data['lms_mb_tg_purple'] = info['tg_purple']

    html_string += styles.description._heading(
        u'MacLeod\u2013Boynton ls chromaticity diagram')
    html_string += (
        styles.description._parameters(data) +
        styles.description._coordinates('\\(l_{\,\mathrm{MB},\,%s,\,%d}\\)' %
                                        (data['field_size'], data['age']),
                                        '\\(m_{\,\mathrm{MB},\,%s,\,%d}\\)' %
                                        (data['field_size'], data['age']),
                                        '\\(s_{\,\mathrm{MB},\,%s,\,%d}\\)' %
                                        (data['field_size'], data['age'])) +
        styles.description._wavelenghts(data) +
        styles.description._normalization_lms_mb(data) +
        styles.description._LMS_to_lms_mb(data, data) +
        styles.description._precision_lms_mb() +
        styles.description._illuminant_E_lms_mb(data) +
        styles.description._purpleline_tangentpoints_lms_mb(data))

    return html_string


def LMS_MW_sidemenu(parameters):
    """
    LMS_MW_sidemenu(...) is directly based description.py, lines 1199-1234.

    Parameters
    ----------
    parameters: Global parameter system, dict of user inputs.

    Returns
    -------
    Generated HTML page with sidemenu contents.

    """
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['λ_min'] = data['min']
    data['λ_max'] = data['max']
    data['λ_step'] = data['step_size']

    # needs info from maxwell, does computation
    data['info'] = True
    info = compute_Maxwellian_modular(data)
    data['norm_coeffs_lms_mw'] = info['norm']
    data['lms_mw_white'] = info['white']
    data['lms_mw_tg_purple'] = info['tg_purple']

    html_string += (styles.description._heading('Maxwellian lm chromaticity diagram') +
                    styles.description._parameters(data) +
                    styles.description._coordinates('\\(l_{\,%s,\,%d}\\)' %
                                                    (data['field_size'],
                                                     data['age']),
                                                    '\\(m_{\,%s,\,%d}\\)' %
                                                    (data['field_size'],
                                                     data['age']),
                                                    '\\(s_{\,%s,\,%d}\\)' %
                                                    (data['field_size'], data['age'])) +
                    styles.description._wavelenghts(data) +
                    styles.description._normalization_lms_mw(data) +
                    styles.description._LMS_to_lms_mw(data) +
                    styles.description._precision_lms_mw() +
                    styles.description._illuminant_E_lms_mw(data) +
                    styles.description._purpleline_tangentpoints_lms_mw(data))

    return html_string


def XYZ_sidemenu(parameters):
    """
    XYZ_sidemenu(...) is directly based on description.py, lines 1237-1271.

    Parameters
    ----------
    parameters: Global parameter system, dict of user inputs.

    Returns
    -------
    Generated HTML page with sidemenu contents.

    """
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['λ_min'] = data['min']
    data['λ_max'] = data['max']
    data['λ_step'] = data['step_size']

    data['info'] = True
    info = compute_XYZ_modular(data)
    # compute_XYZ_modular makes the trans_mat itself either normal or not normalized, depending on
    # the value of parameters['norm']; if it is activated, 'trans_mat' is normalized, so it makes sure
    # that either way, it gets the right one
    data['trans_mat'] = info['trans_mat']
    data['trans_mat_N'] = info['trans_mat']

    html_string += (styles.description._heading('CIE XYZ cone-fundamental-based tristimulus functions') +
                    styles.description._parameters(data) +
                    styles.description._functions('\\(\\bar x_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                                  (data['field_size'],
                                                   data['age']),
                                                  '\\(\\bar y_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                                  (data['field_size'],
                                                   data['age']),
                                                  '\\(\\bar z_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                                  (data['field_size'],
                                                   data['age']),
                                                  '\\(\\lambda\\) &nbsp;(wavelength)') +
                    styles.description._wavelenghts(data) +
                    styles.description._normalization_XYZ(data, data) +
                    styles.description._LMS_to_XYZ(data, data) +
                    styles.description._precision_XYZ()
                    )
    return html_string


def XY_sidemenu(parameters):
    """
    XY_sidemenu(...) is directly based on description.py, lines 1274-1309.

    Parameters
    ----------
    parameters: Global parameter system, dict of user inputs.

    Returns
    -------
    Generated HTML page with sidemenu contents.

    """
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['λ_min'] = data['min']
    data['λ_max'] = data['max']
    data['λ_step'] = data['step_size']

    data['info'] = True
    info = compute_XY_modular(data)
    # same as XYZ, the 'xyz_white' in info is equal to both normalized and unnormalized value of xyz_white,
    # depending on the true/false of parameters['norm'] (copied to data, so data['norm']
    data['xyz_white'] = info['xyz_white']
    data['xyz_white_N'] = info['xyz_white']
    data['xyz_tg_purple'] = info['xyz_tg_purple']
    data['xyz_tg_purple_N'] = info['xyz_tg_purple']

    html_string += (
        styles.description._heading("CIE xy cone-fundamental-based chromaticity diagram") +
        styles.description._parameters(data) +
        styles.description._coordinates('\\(x_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                        (data['field_size'], data['age']),
                                        '\\(y_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                        (data['field_size'], data['age']),
                                        '\\(z_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                        (data['field_size'], data['age'])) +
        styles.description._wavelenghts(data) +
        styles.description._normalization_xyz(data, data) +
        styles.description._XYZ_to_xyz(data) +
        styles.description._precision_xyz() +
        styles.description._illuminant_E_xyz(data, data) +
        styles.description._purpleline_tangentpoints_xyz(data, data)
    )
    return html_string


def XYZP_sidemenu(parameters):
    """
    XYZP_sidemenu(...) is directly based on description.py, lines 1312-1349.

    Parameters
    ----------
    parameters: Global parameter system, dict of user inputs.

    Returns
    -------
    Generated HTML page with sidemenu contents.

    """
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['λ_min'] = data['min']
    data['λ_max'] = data['max']
    data['λ_step'] = data['step_size']

    data['info'] = True
    info = compute_XYZ_modular(data)
    # compute_XYZ_modular makes the trans_mat itself either normal or not normalized, depending on
    # the value of parameters['norm']; if it is activated, 'trans_mat' is normalized, so it makes sure
    # that either way, it gets the right one
    data['trans_mat'] = info['trans_mat']
    data['trans_mat_N'] = info['trans_mat']

    # also needs result from computation of itself to get these values
    data['info'] = False
    purples = compute_XYZ_purples_modular(data)['result']
    data['λ_purple_min'] = '%.1f' % purples[0, 0]
    data['λ_purple_max'] = '%.1f' % purples[-1, 0]
    data['λ_purple_min_N'] = data['λ_purple_min']
    data['λ_purple_max_N'] = data['λ_purple_max']

    html_string += (
        styles.description._heading("XYZ cone-fundamental-based tristimulus functions for purple-line stimuli") +
        styles.description._parameters(data) +
        styles.description._functions(
            '\\(\\bar x_{\,\mathrm{Fp},\,%s,\,%d}\\)' %
            (data['field_size'], data['age']),
            '\\(\\bar y_{\,\mathrm{Fp},\,%s,\,%d}\\)' %
            (data['field_size'], data['age']),
            '\\(\\bar z_{\,\mathrm{Fp},\,%s,\,%d}\\)' %
            (data['field_size'], data['age']),
            '<nobr>\\(\\lambda_{\\mathrm{c}}\\)</nobr> \
                            &nbsp;(complementary<font size="0.0em"> </font>\
                            &nbsp;wavelength)') +
        styles.description._wavelenghts_complementary(data, data) +
        styles.description._normalization_XYZ(data, data) +
        styles.description._LMS_to_XYZ_purples(data, data) +
        styles.description._precision_XYZ()
    )
    return html_string


def XYP_sidemenu(parameters):
    """
    LMS_sidemenu(...) is directly based on description.py, lines 1352-1387.

    Parameters
    ----------
    parameters: Global parameter system, dict of user inputs.

    Returns
    -------
    Generated HTML page with sidemenu contents.

    """
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['λ_min'] = data['min']
    data['λ_max'] = data['max']
    data['λ_step'] = data['step_size']

    data['info'] = True
    info = compute_XY_modular(data)
    # same as XYZ, the 'xyz_white' in info is equal to both normalized and unnormalized value of xyz_white,
    # depending on the true/false of parameters['norm'] (copied to data, so data['norm']
    data['xyz_white'] = info['xyz_white']
    data['xyz_white_N'] = info['xyz_white']
    data['xyz_tg_purple'] = info['xyz_tg_purple']
    data['xyz_tg_purple_N'] = info['xyz_tg_purple']

    # also needs result from computation of itself to get these values
    data['info'] = False
    purples = compute_XYZ_purples_modular(data)['result']
    data['λ_purple_min'] = '%.1f' % purples[0, 0]
    data['λ_purple_max'] = '%.1f' % purples[-1, 0]
    data['λ_purple_min_N'] = data['λ_purple_min']
    data['λ_purple_max_N'] = data['λ_purple_max']

    html_string += (
        styles.description._heading("xy cone-fundamental-based chromaticity diagram (purple-line stimuli)") +
        styles.description._parameters(data) +
        styles.description._coordinates('\\(x_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                        (data['field_size'], data['age']),
                                        '\\(y_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                        (data['field_size'], data['age']),
                                        '\\(z_{\,\mathrm{F},\,%s,\,%d}\\)' %
                                        (data['field_size'], data['age'])) +
        styles.description._wavelenghts_complementary(data, data) +
        styles.description._normalization_xyz(data, data) +
        styles.description._XYZ_purples_to_xyz_purples(data) +
        styles.description._precision_xyz() +
        styles.description._illuminant_E_xyz(data, data) +
        styles.description._purpleline_tangentpoints_xyz_complementary(
            data, data)
    )
    return html_string


def XYZ_std_sidemenu(parameters):
    """
    LMS_sidemenu(...) is directly based on LMS(...) from description.py, lines 1390-1454.

    Parameters
    ----------
    parameters: Global parameter system, dict of user inputs.

    Returns
    -------
    Generated HTML page with sidemenu contents.

    """
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible

    html_string += styles.description._heading(
        "CIE XYZ standard colour-matching functions")

    # description.py, lines 1390-1420
    if data['field_size'] == cieapi.STD_1931:
        html_string += (
            styles.description._parameters_std('2') +
            styles.description._functions('\\(\\bar x\\) ',
                                          '\\(\\bar y\\) ',
                                          '\\(\\bar z\\)',
                                          '\\(\\lambda\\) &nbsp;(wavelength)') +
            styles.description._wavelenghts_std() +
            styles.description._normalization_XYZ31() +
            styles.description._precision_XYZ()
        )
    else:
        # description.py, lines 1423-1454
        html_string += (
            styles.description._parameters_std('10') +
            styles.description._functions('\\(\\bar x_{10}\\)',
                                          '\\(\\bar y_{10}\\)',
                                          '\\(\\bar z_{10}\\)',
                                          '\\(\\lambda\\) &nbsp;(wavelength)') +
            styles.description._wavelenghts_std() +
            styles.description._normalization_XYZ64() +
            styles.description._precision_XYZ()
        )
    return html_string


def XY_std_sidemenu(parameters):
    """
    LMS_sidemenu(...) is directly based on LMS(...) from description.py, lines 1457-1522.

    Parameters
    ----------
    parameters: Global parameter system, dict of user inputs.

    Returns
    -------
    Generated HTML page with sidemenu contents.

    """
    html_string = ""
    html_string += _head()

    # copy of parameters to allow for changes without modifying original
    data = parameters.copy()
    # changing their names to be equal to 'data' and 'options' keys, so that it
    # can use as much of the original material as possible
    data['info'] = True
    info = compute_xyz_standard_modular(data)
    # the info 'tg_purple' is applied to both for same reason normalization is above;
    #
    data['xyz31_tg_purple'] = info['tg_purple']
    data['xyz64_tg_purple'] = info['tg_purple']

    html_string += styles.description._heading(
        "CIE xy standard chromaticity diagram")
    # description.py, lines 1457-1487
    if data['field_size'] == cieapi.STD_1931:
        html_string += (
            styles.description._parameters_std('2') +
            styles.description._coordinates('\\(x\\)', '\\(y\\)', '\\(z\\)') +
            styles.description._wavelenghts_std() +
            styles.description._normalization_xyz31() +
            styles.description._XYZ31_to_xyz31() +
            styles.description._precision_xyz() +
            styles.description._illuminant_E_xyz31() +
            styles.description._purpleline_tangentpoints_xyz31(data)
        )
    else:
        # description.py, lines 1490-1522
        html_string += (
            styles.description._parameters_std('10') +
            styles.description._coordinates('\\(x_{10}\\)',
                                            '\\(y_{\,10}\\)',
                                            '\\(z_{\,10}\\)') +
            styles.description._wavelenghts_std() +
            styles.description._normalization_xyz64() +
            styles.description._XYZ64_to_xyz64() +
            styles.description._precision_xyz() +
            styles.description._illuminant_E_xyz64() +
            styles.description._purpleline_tangentpoints_xyz64(data)
        )
    return html_string
