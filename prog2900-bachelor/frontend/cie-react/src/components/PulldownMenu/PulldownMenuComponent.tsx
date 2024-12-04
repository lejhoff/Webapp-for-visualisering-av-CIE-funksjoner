/*PullDownMenuComponent.tsx: Renders PulldownMenu component

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
import './PulldownMenu.css';
import { useContentController } from '../../hooks/useContentController';

/**
 * React functional component that renders a PulldownMenu allowing the user to select which
 * function they want to inspect.
 * @returns {JSX.Element} Renders PulldownMenu as a JSX Element
 */
export const PulldownMenu: React.FC = () => {
  const { setSelectedOption } = useContentController();

  return (
    <div className="pulldownMenu">
      <select className="pulldownSelect" onChange={(e) => setSelectedOption(e.target.value)}>
        <option value="method1">CIE LMS cone fundamentals</option>
        <option value="method2">CIE LMS cone fundamentals (9 sign. figs.)</option>
        <option value="method3">MacLeod-Boynton Is chromaticity diagram</option>
        <option value="method4">Maxwellian Im chromaticity diagram</option>
        <option value="method5">CIE XYZ cone-fundamental-based tristimulus functions</option>
        <option value="method6">CIE xy cone-fundamental-based chromaticity diagram</option>
        <option value="method7">XYZ cone-fundamental-based tristimulus functions for purple-line stimuli</option>
        <option value="method8">xy cone-fundamental-based chromaticity diagram (purple-line stimuli)</option>
        <option value="method9">CIE XYZ standard colour-matching functions</option>
        <option value="method10">CIE xy standard chromaticity diagram</option>
      </select>
    </div>
  );
};