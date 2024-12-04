/*NavbarComponent.tsx: Renders Navbar component

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
import { Link } from 'react-router-dom';
import './navbar.css'
import { PLOT_ROUTE, TABLE_ROUTE } from '../../utils/router-urls';

/**
 * React functional component that renders a navigation bar using react-router-dom.
 * Provides links to routes to the application: plot and table. When clicked this routes to the respective
 * component that the user wants to display.
 * @returns {JSX.Element} Navbar component as a JSX element
 */
const Navbar = () => {
    return (
        <nav className="navbar">
            <ul className="navbar-list">
                <li className="navbar-item"><Link to={PLOT_ROUTE}>Plot</Link></li>
                <li className="navbar-item"><Link to={TABLE_ROUTE}>Table</Link></li>
            </ul>
        </nav>
    );
}

export default Navbar;