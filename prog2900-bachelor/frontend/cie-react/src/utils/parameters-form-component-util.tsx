/*parameters-form-component-util.tsx: Specifies rules for
validation of user input

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
import * as yup from 'yup'

/**
 * Defines the rules for input validation in the parametersform.
 */
export const parameterSchema = yup.object().shape({
    field_size: yup.number()
      .required('Field size is required')
      .min(1.0, 'Field size must be greater than 1.0')
      .max(10.0, 'Field size must be less than 10.0'), 
    age: yup.number()
      .required('Age is required')
      .min(20, 'Age must be greater than 20')
      .max(80,  'Age must be less than 80'), 
    min: yup.number()
      .required('Min domain is required')
      .min(390.0, 'Min domain must be greater than 390.0')
      .max(400.0, 'Min domain must be less than 400.0'),
    max: yup.number()
      .required('Max domain is required')
      .min(700.0, 'Max domain must be greater than 700.0')
      .max(830.0, 'Max domain must be less than 830.0'),
    step_size: yup.number()
      .required('Step size is required')
      .min(1.0, 'Step size must be greater than 1.0')
      .max(5.0, 'Step size must be less than 5.0')
  });