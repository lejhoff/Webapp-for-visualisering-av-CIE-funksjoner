/*App.tsx: Application component

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

import { createHashRouter, Navigate, Outlet, RouterProvider } from "react-router-dom";
import Navbar from "./components/navbar/NavbarComponent.tsx";
import { PLOT_ROUTE, TABLE_ROUTE } from "./utils/router-urls.tsx";
import TableContent from "./components/table/TableComponent.tsx";
import ParametersLayout from "./components/parameters/ParametersLayoutComponent.tsx";
import { ParametersProvider } from './context/parameter-context.tsx';
import { UseContentControllerProvider } from "./hooks/useContentController.tsx";
import PlotIframe from "./components/Iframe/PlotIframeComponent.tsx";
import RightSideMenuComponent from "./components/Iframe/BottomSideMenuComponent.tsx";
import BottomSideMenuComponent from "./components/Iframe/RightSideMenuComponent.tsx";

/**
 * Application component that sets up routing, context providers.
 *  
 * @returns {JSX.Element} The application component with routing and context providers.
 */
function App() {
  
  const router = createHashRouter([
    {
      path: "/",
      element: (
        <UseContentControllerProvider>
          <ParametersProvider>
            <Navbar />
            <div className="outer-container">
              <Outlet />
            </div>
          </ParametersProvider>
        </UseContentControllerProvider>
      ),
      children: [
        { path: "", element: <Navigate to={PLOT_ROUTE} replace /> },
        { path: PLOT_ROUTE, element: <div className="inner-container">
        <div className="plo">
          <ParametersLayout><PlotIframe/></ParametersLayout>
          < RightSideMenuComponent/>
        </div>
        < BottomSideMenuComponent/>
        </div> },
        { path: TABLE_ROUTE, element: <div className="inner-container">
        <div className="tab">
          <ParametersLayout><TableContent/></ParametersLayout>
          < RightSideMenuComponent/>
        </div>
        < BottomSideMenuComponent/>
      </div> },
      ],
    }
  ]);

  return <RouterProvider router={router} />;
}

export default App;
