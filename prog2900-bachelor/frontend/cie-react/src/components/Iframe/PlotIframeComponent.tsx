/*PlotIframeComponent.tsx: Renders iframe component for plot

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
import { useParameters } from "../../context/parameter-context";
import LoadingIndicator from "../LoadingIndicator";
import IframeComponent from "./IframeComponent";

/**
 * React functional component that renders an iframe from the given url.
 * Renders an IframeComponent from the '/plot' endpoint of the backend API. 
 * Serves as the plot component.
 * @returns {JSX.Element} Renders the LoadingIndicator during the fetching process.
 * Rendered plot iframe component if plotUrl exists, otherwise returns null.
 */
const PlotIframe: React.FC = () => {
    const { plotUrl, isLoading } = useParameters();

    if (isLoading) {
        return <LoadingIndicator />;
      }

    return (
        plotUrl && <IframeComponent iframe_url={plotUrl} />
    );
  };
  
  export default PlotIframe;