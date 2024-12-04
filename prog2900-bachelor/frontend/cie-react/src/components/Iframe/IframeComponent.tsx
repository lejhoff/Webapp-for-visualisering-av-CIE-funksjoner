/*IframeComponent.tsx: Renders iframe component

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

/**
 * Prop for IframeComponent
 * @property {string} iframe_url The url from where the iframe is
 * fetched from the backend API.
 */
type IframeProps = {
  iframe_url: string;
};

/**
 * React functional component that renders and iframe from the given url.
 * Provides 
 * @param {IframeProps} props The props for the component
 * @returns {JSX.Element} Rendered iframe component.
 */
const IframeComponent: React.FC<IframeProps> = ({ iframe_url }) => {
  return (
    <iframe
      src={iframe_url}
      style={{ width: '100%', height: '100%', border: 'none'}}
      title="iframe-component"
      allowFullScreen
    ></iframe>
  );
};

export default IframeComponent;