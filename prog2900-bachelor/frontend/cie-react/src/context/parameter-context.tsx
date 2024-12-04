/*parameter-context.tsx: Creates and handles context for parameters

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
import { createContext, useContext, useState, ReactNode, useCallback } from 'react';
import { Parameters, ComputedData, ParametersContextType } from '../utils/prop-types';
import { fetchApiData } from '../utils/api-service';
import { useLoading } from '../hooks/useLoading';
import { stringBuilder } from '../utils/string-builder';

/**
 * Default values for the context of parameters and functions
 * related to the context of parameters.
 */
const defaultContextValue: ParametersContextType = {
  parameters: {
    field_size: 2.0,
    age: 32,
    min: 390.0,
    max: 830.0,
    step_size: 1.0,
  },
  setParameters: () => {},
  computedData : {
    tableData: []
  },
  setComputedData: () => {},
  computeData: async () => {},
  isLoading: true,
  endpoint: '',
  setEndpoint: () => {},
  plotUrl: '',
  setPlotUrl: () => {},
  sidemenuUrl: '',
  setSidemenuUrl: () => {}

};

/**
 * Creates a context with default values. Contains a set of functions to help manipulate
 * parameter state.
 * 
 * Exports ParameterProvider which wraps children and allows for state handling of
 * parameters through the applicaiton.
 */
const ParametersContext = createContext<ParametersContextType>(defaultContextValue);
export const useParameters = () => useContext(ParametersContext);
export const ParametersProvider = ({ children }: { children?: ReactNode }) => {
  const [parameters, setParameters] = useState<Parameters>(defaultContextValue.parameters);
  const [computedData, setComputedData] = useState<ComputedData>(defaultContextValue.computedData);
  const { isLoading, stopLoading } = useLoading();
  const [endpoint, setEndpoint] = useState<string>('lms/');
  const [plotUrl, setPlotUrl] = useState<string>('');
  const [sidemenuUrl, setSidemenuUrl] = useState<string>('');

  //fetches the iframe for sidemenu and plot from the backend API
  const updateIframes = useCallback(async () => {
    try {
      const plotUrl = stringBuilder(endpoint + 'plot', parameters);
      const menuUrl = stringBuilder(endpoint + 'sidemenu', parameters);
      setPlotUrl(plotUrl);
      setSidemenuUrl(menuUrl);
    } catch (error) {
      console.error('Error fetching plot content:', error);
    }
  }, [endpoint, parameters]);

  //fetches the result data from the backend API
  //to be displayed in the TableComponent
  const computeData = useCallback(async () => {
    const calculateData = endpoint + 'calculation';
    try {
      console.log("Current parameters:", parameters);
      const { result } = await fetchApiData(calculateData, parameters);
      setComputedData({ tableData: result});
      updateIframes();
    } catch (error) {
      console.error('Error:', error);
    } finally {
      stopLoading();
    }
  }, [endpoint, parameters]);

  return (
    <ParametersContext.Provider value={{ parameters, setParameters, computedData, setComputedData, computeData, isLoading, endpoint, setEndpoint, plotUrl, setPlotUrl, sidemenuUrl, setSidemenuUrl }}>
      {children}
    </ParametersContext.Provider>
  );
};
