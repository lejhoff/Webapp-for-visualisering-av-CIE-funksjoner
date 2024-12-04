/*RightSideMenuComponent.tsx: For rendering sidemenu
under parameterform based on the current screen width

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

import { useScreenWidth } from "../../hooks/useScreenWidth";
import SideMenuIframe from "./SideMenuIframeComponent";

/**
 * React functional component for rendering the sidemenu when it is to be placed to the right of the plot/table
 * @returns  {JSX.Element} The rendered sidemenu iframe if the screen width is more than 1200px.
 */
const RightSideMenuComponent: React.FC = () => {
    const screenWidth = useScreenWidth();
    return (
      <>
        {screenWidth > 1200 && (
          <div className="sid">
            <SideMenuIframe />
          </div>
        )}
      </>
    );
  };
  export default RightSideMenuComponent;