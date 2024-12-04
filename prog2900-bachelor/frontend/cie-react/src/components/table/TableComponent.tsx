/*TableComponent.tsx: Renders TableComponent

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

import './table.css';
import { useParameters } from '../../context/parameter-context';
import LoadingIndicator from '../LoadingIndicator';


/**
 * React functinoal component to construct the table with the computed data.
 * Takes the JSON response from the api call and puts the result.data into 
 * the table
 * @returns {JSX.Element} TableContent as JSX Element
 */
const TableContent = () => {
  const { computedData, isLoading } = useParameters();

  if (isLoading) {
    return <LoadingIndicator />;
  }

  return (
    <div className="scrollable-table">
      <table>
        <thead>
          <tr>
            <th>X</th>
            <th>Y 1</th>
            <th>Y 2</th>
            <th>Y 3</th>
          </tr>
        </thead>
        <tbody>
          {computedData.tableData.map((row, index) => (
            <tr key={index}>
              {row.map((cell, cellIndex) => (
                <td key={cellIndex}>{cell}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};


export default TableContent;
