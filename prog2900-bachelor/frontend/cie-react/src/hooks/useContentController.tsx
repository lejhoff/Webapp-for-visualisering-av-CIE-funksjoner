/*useContentController.tsx: Manages state for selected method

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
import { ReactNode, createContext, useContext, useState } from 'react';

/**
 * Defines the shape of the hook returned by conent controller context
 * @property {string} selectedOption Currently selected option for color match function.
 * @property {function} setSelectedOption Function to update the selected option.
 */
type UseContentControllerHook = {
  selectedOption: string;
  setSelectedOption: (option: string) => void;
};

const ContentControllerContext = createContext<UseContentControllerHook | undefined>(undefined);

/**
 * Provider component that manages state related to the selected option for  function.
 * Wraps children to allow access for the context value.
 * @param {ReactNode} children child components that will get access to context values.
 * @returns {JSX.Element} Provider component as JSX Element that provides context values regarding selectod method for its children.
 */
export const UseContentControllerProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [selectedOption, setSelectedOption] = useState<string>("method1");

  return (
    <ContentControllerContext.Provider value={{ selectedOption, setSelectedOption }}>
      {children}
    </ContentControllerContext.Provider>
  );
};

export const useContentController = (): UseContentControllerHook => {
  const context = useContext(ContentControllerContext);
  if (context === undefined) {
    throw new Error('Error!! useContentController without context!!');
  }
  return context;
};