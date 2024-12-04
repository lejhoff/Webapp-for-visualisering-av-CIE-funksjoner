/*string-builder.tsx: Builds the urls for API calls

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
along with this program.  If not, see http://www.gnu.org/licenses/.
*/

import { API_BASE_URL } from "./api-urls";
import { Parameters } from "./prop-types";

/**
 * Function for building the url strings based ont he variable endpoint and parameters.
 * Constructs the complete URL by appending the endpoint to the base url and adding query parameters.
 * @param endpoint The endpoint defined by the specified function.
 * @param params The parameters specified by the user.
 * @returns {string} The constructed URL as a string.
 */
function stringBuilder(endpoint: string, params: Parameters): string {
    const queryParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined) {
            queryParams.append(key, value.toString());
        }
    });
  
    return `${API_BASE_URL}${endpoint}?${queryParams.toString()}`;
  }
  export { stringBuilder};