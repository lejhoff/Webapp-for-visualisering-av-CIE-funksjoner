# Tests

## Current Coverage

### v2
- Date: 16/04/2024, 19:19
```
Name                       Stmts   Miss  Cover   
------------------------------------------------
cieapi.py                    231     43    81%  
cieapi_test.py               112      2    98%   
compute.py                   559    299    47%   
computemodularization.py     195     20    90%   
utils.py                      11      0   100%
------------------------------------------------
TOTAL                       1108    364    67%
```

### v1
- Date: 15/04/2024, 21:10

```
raw (from .coverage file):

Name                       Stmts   Miss  Cover
----------------------------------------------
cieapi.py                    206     31    85%
compute.py                   559    318    43%
computemodularization.py     195     26    87%
tests\cieapi_test.py         112      2    98%
utils.py                      11      0   100%
----------------------------------------------
TOTAL                       1083    377    65%

==============================================

not including compute.py (calculated):

Name                       Stmts   Miss  Cover
----------------------------------------------
cieapi.py                    206     31    85%
computemodularization.py     195     26    87%
tests\cieapi_test.py         112      2    98%
utils.py                      11      0   100%
----------------------------------------------
TOTAL                        524     59    89% (88.74%)

==============================================

only including cieapi.py and computemodularization.py:

Name                       Stmts   Miss  Cover
----------------------------------------------
cieapi.py                    206     31    85%
computemodularization.py     195     26    87%
----------------------------------------------
TOTAL                        401     57    86% (85.78%)
```
## `csv` documentation

This part contains the parameters used for the `csv` files in the unit testing of
the endpoints. 

- `LMS-1-25-1.csv`:
  - LMS, field size of 1, age of 25, step size of 1.
- `LMS-1-25-01.csv`:
  - LMS, field size of 1, age of 25, step size of 0.1.
- `LMS-2-20-1-log-base.csv`:
  - LMS, field size of 2, age of 20, step size of 1, with log10 and base parameters activated.
- `LMS-MB-5-63-1.csv`:
  - Macleod, field size of 5, age of 63, step size of 1.
- `LMS-MB-5-63-01.csv`:
  - Macleod, field size of 5, age of 63, step size of 0.1.
- `LMS-MW-45-45-1.csv`:
  - Maxwellian, field size of 4.5, age of 45, step size of 1.
- `LMS-MW-45-45-01.csv`:
  - Maxwellian, field size of 4.5, age of 45, step size of 0.1.
- `XY-31-71-01.csv`:
  - XY, field size of 3.1, age of 71, step size of 0.1.
- `XY-31-71-10.csv`:
  - XY, field size of 3.1, age of 71, step size of 1.
- `XY-STD-2.csv`:
  - XY standardization function, field size of 2.
- `XYP-20-32-1.csv`:
  - XY-purple, field size of 2.0, age of 32, step size of 1.
- `XYP-20-32-01.csv`:
  - XY-purple, field size of 2.0, age of 32, step size of 0.1.
- `XYZ-38-52-01.csv`:
  - XYZ function, field size of 3.8, age of 52, step size of 0.1.
- `XYZ-38-52-15.csv`:
  - XYZ function, field size of 3.8, age of 52, step size of 1.5.
- `XYZ-STD-2.csv`:
  - XYZ standardization function, field size of 2.