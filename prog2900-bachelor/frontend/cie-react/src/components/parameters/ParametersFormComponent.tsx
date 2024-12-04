/*ParametersFormComponent.tsx: Renders parameters form component

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

import React, { ChangeEvent, useEffect, useState } from 'react';
import { useParameters } from '../../context/parameter-context';
import './parameters-form.css'
import { endpointMap } from '../../utils/prop-types';
import { LMS_URL } from '../../utils/api-urls';
import { useContentController } from '../../hooks/useContentController';
import { parameterSchema } from '../../utils/parameters-form-component-util';

/**
 * React functional component that renders the parametersform. Creates the parameterform based on the selected function,
 * and renders a parameterform with the needed elements for userinput. 
 * 
 * Renders parameter form with a dropdown menu for field size
 * 
 * Renders parameter form with input fields for field size, age, min and max for domain size and step size and a 
 * compute button for every other colormatch function.
 * @returns {JSX.Element} ParametersForm as a JSX element.
 */
const ParametersForm: React.FC = () => {
  const { parameters, setParameters, computeData, setEndpoint, endpoint } = useParameters();
  const { selectedOption } = useContentController();
  const [generalFieldSize, setGeneralFieldSize] = useState(parameters.field_size);
  const [dropdownFieldSize, setDropdownFieldSize] = useState(parameters.field_size);
  const [paramsUpdated, setParamsUpdated] = useState(false);

  //useeffect to set new endpoint based on selected option in pulldown
  useEffect(() => {
    const newEndpoint = endpointMap[selectedOption] || LMS_URL;
    setEndpoint(newEndpoint);
  }, [selectedOption, setEndpoint]);

   //useeffect to use generalFieldSize for function 1-8 and dropDownFieldSize 
   //for function 9 and 10. State handling for the two different field sizes
   //handles the logic for adding a optional parameter 'base' if the selected
   //is method2
   useEffect(() => {
    const methodNumber = parseInt(selectedOption.replace('method', ''));
    setParameters(prev => {
      const updatedParams = { ...prev };

      // Handle optional parameter for method2
      if (selectedOption === 'method2') {
        updatedParams.optional = 'base';
      } else {
        delete updatedParams.optional;
      }

      // Handle field size based on method number
      if (methodNumber >= 1 && methodNumber <= 8) {
        updatedParams.field_size = generalFieldSize;
      } else if (methodNumber >= 9 && methodNumber <= 10) {
        updatedParams.field_size = dropdownFieldSize;
      }

      return updatedParams;
    });
    setParamsUpdated(true);
  }, [selectedOption, dropdownFieldSize, setParameters]);

  //useffect to call computedata when endpoint is changed or when dropDownFieldSize is changed
  useEffect(() => {
    if (paramsUpdated) {
      computeData();
      setParamsUpdated(false);
    }
}, [endpoint, selectedOption, paramsUpdated, setParameters, computeData]);

  //Handles parameter change for every function except xyz
  const handleParameterChange = (event: ChangeEvent<HTMLInputElement>): void => {
    const { name, value } = event.target;
    const numericValue = parseFloat(value);
    
    //validates the user specified input
    parameterSchema.validateAt(name, { [name]: numericValue })
      .then(() => {
        if (name === 'field_size') {
          setGeneralFieldSize(numericValue);
        }
        setParameters(prev => ({ ...prev, [name]: numericValue }));
      })
      .catch(err => {
        console.error(err.errors);
      });
  };
  
  //Handles parameter change for xyz functions, where field size of either 2 or 10 degrees are the parameters
  const handleDropdownChange = (event: ChangeEvent<HTMLSelectElement>): void => {
    const selectedDegree = parseFloat(event.target.value);
    setDropdownFieldSize(selectedDegree);
    setParameters(prev => ({ ...prev, field_size: selectedDegree }));
    setParamsUpdated(true);
  };

  //Creates the parametercontrols for the parameters form. These are the string and input fields for a given parameter in the form.
  const createParameterControl = (label: string, name: string, value: number, onChange: (event: ChangeEvent<HTMLInputElement>) => void) => (
    <div className="parametersControl">
      <label className="parameterLabel" htmlFor={name}>{label}</label>
      <input
        type="number"
        className="formControl"
        id={name}
        name={name}
        value={name === "age" ? value.toString() : value.toFixed(1)}
        onChange={onChange}
        step={name === "age" ? 1 :  0.1}
      />
    </div>
  );

  //Creates the dropdown menu for selecting field size for the two
  //standard functions; method9 and method 10
  const createDegreeDropdown = () => (
    <div className="parametersControl">
      <label htmlFor="degree-selection">Field size:	</label>
      <select
        className="formControl"
        id="degree-selection"
        name="degree-selection"
        value={dropdownFieldSize.toString()}
        onChange={handleDropdownChange}
      >
        <option value="2">2°</option>
        <option value="10">10°</option>
      </select>
    </div>
  );

  //Creates the parameter form with the required fields for userinput. 
  const createParameterForm = () => {
    return(<div className="parametersForm">
      {createParameterControl("Field size:", "field_size", generalFieldSize, handleParameterChange)}
      {createParameterControl("Age:", "age", parameters.age, handleParameterChange)}
      {createParameterControl("Domain min(nm):", "min", parameters.min, handleParameterChange)}
      {createParameterControl("Domain max (nm):", "max", parameters.max, handleParameterChange)}
      {createParameterControl("Step(nm):", "step_size", parameters.step_size, handleParameterChange)}
      <button className="btnPrimary" onClick={computeData}>Compute</button>
    </div>
    );
  }

  //Takes in the selected color matching function, parses the method name to determine
  //which method it is and decides which parameters form to display:
  //- For method 1-8 the createParametersForm is displayed. This contains option for 
  //  field_size(1-10), age, domain min and max, step size
  //- For method 9 and 10 the createDegreeDropDown is displayed. This only contains
  //  the dropdown menu for selecting 2 or 10 as field_size 
  const renderParameters = () => {

     const methodNumber = parseInt(selectedOption.replace('method', ''));
    if (methodNumber >= 1 && methodNumber <= 8) {
      return createParameterForm();
    } else if (methodNumber >= 9 && methodNumber <= 10) {
      return createDegreeDropdown();
    }
    return <p>Please select a method to display parameters.</p>;
  };

  return (
    <div className="parametersForm">
        {renderParameters()}
    </div>
  );
};

export default ParametersForm;
