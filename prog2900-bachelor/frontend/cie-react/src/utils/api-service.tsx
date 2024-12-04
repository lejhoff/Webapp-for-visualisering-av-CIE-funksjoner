/*api-service.tsx: Provides utility for API calls

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

import { ApiResponse, Parameters } from "./prop-types";
import { stringBuilder } from "./string-builder";



/**
 * Fetches data from the backend API.
 * 
 * Constructs url with the help of the stringbuilder utils function and the parameters
 * 'endpoint' and 'params' that it receives. Makes a GET request to the bakcend API
 * at the constructed URL
 * @param {string} endpoint The API endpoint to fetch data from. This corresponds to the selected color match function
 * @param {Parameters} params The user specified parameters to be included in the API request
 * @returns {Promise<ApiResponse>} Returns the result from the API request and promises the format to correspond to ApiRespone
 */
async function fetchApiData(endpoint: string, params: Parameters): Promise<ApiResponse> {
  const url = stringBuilder(endpoint, params);
  console.log(url);
  const response = await fetch(url, {
    method: 'GET',
    headers: { 'Content-Type': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response.json().then(data => {
    if (data.result && data.plot) {
      return { result: data.result};
    } else {
      throw new Error('Unexpected response structure');
    }
  });
}
export {fetchApiData}

