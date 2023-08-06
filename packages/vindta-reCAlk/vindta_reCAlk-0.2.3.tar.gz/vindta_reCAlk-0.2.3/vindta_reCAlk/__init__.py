"""
VINDTA reCAlk
=============
*VINTDA recalculate diC and Alkalinity*


USAGE
-----
This script is for reading in output from a VINDTA.

1) Read in the .dbs file and associated .dat files with
   the `dbs_to_excel()` function. The script creates an
   excel file if a filename is given, else only a
   `pandas.DataFrame` is returned.
2) Columns for nutrients are added to the excel file.
   These should be filled out before running the second
   recalculation step where CRMs are used to calibrate
   the data.
3) Run the CRM recalculation step with the function
   `recalculate_CO2_from_excel`. The recalculation
   is performed without you having to do anything :)
   The data will be saved in the excel file in a
   second tab.


NOTES
-----
This was written for the CSIR's VINDTA #18 and #35.
There are thus headers that may need to be changed.
These headers can be changed manually in the dbs_to_excel
function using the header keyword argument. Be very
careful when changing this. It needs to match your
VINDTA's column headers.


TO DO
-----
- add documentation for the functions. A little sparse at the moment.
- write additional info in the output excel file.


INFORMATION
-----------
Version: 0.2
Author:  Luke Gregor
Email:   lukegre@gmail.com
Date:    2018-06-14

This script was written independently and was not funded by the
CSIR (where Luke was working at the time of writing the code).
"""
from __future__ import print_function, unicode_literals, absolute_import

from flask import Flask
from .views import vindta

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = 'super secret key'

app.register_blueprint(vindta)
