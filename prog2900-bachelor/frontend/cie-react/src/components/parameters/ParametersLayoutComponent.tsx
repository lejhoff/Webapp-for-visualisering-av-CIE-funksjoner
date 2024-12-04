/*ParametersLayoutComponent.tsx: Creates layout for parameter related
UI elements

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
import React from 'react';
import ParametersForm from './ParametersFormComponent';
import { PulldownMenu } from '../PulldownMenu/PulldownMenuComponent';
import './parameters-form.css';

/**
 * Interface to define the props for ParametersLayoutComponent
 */
interface LayoutProps {
  children?: React.ReactNode;
}
/**
 * React functional component that creates a layout for displaying parameter related UI elements.
 * Wraps children, which as per implementation means that plot and sidemenu can be wrapped, allowing
 * for dynamic rendering of children components.
 * 
 * Also displays parametersform and pulldownmenu for allowing the user to specify parameters
 * and selecting which colormatch function to inspect. 
 * @param {LayoutProps} props  
 * @returns {JSX.Element} ParametersLayoutCompontent as a JSX Element. Dynamically renders children, then
 * PulldownMenu and ParametersForm
 */
const ParametersLayout: React.FC<LayoutProps> = ({ children }) => {
  return (
    <>
      {children}
      <div className="parameterCard">
        <PulldownMenu />
        <ParametersForm  />
      </div>
    </>
  );
};
export default ParametersLayout;