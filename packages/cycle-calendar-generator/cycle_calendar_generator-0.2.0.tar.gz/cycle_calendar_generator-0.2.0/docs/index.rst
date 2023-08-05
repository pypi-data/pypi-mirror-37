Cycle Calendar Generator - Making school calendars easy
=======================================================

Cycle Calendar Generator is a command line application designed to take schedule data for *n*-day cycles and produce iCal files, ready to import into the calendar software of your choice.

Is your school on a 6-day cycle? 7-day? Cycle Calendar Generator can make iCal files for all your teachers or students!

Quickstart
==========

Assuming you have Python 3.5+ installed, use `pip3 <http://www.pip-installer.org/>`. ::

    $ pip3 install cycle_calendar_generator

Set up your schedule data Excel files as shown in the :ref:`examples`.
Put them all in one folder, and run Cycle Calendar Generator from the command line/Terminal.::

    $ cycle_calendar_generator path/to/excel/files

If you're running the Generator from that folder, no folder input is needed! ::

    $ cycle_calendar_generator

Find your iCal files in the /output folder (i.e. path/to/excel/files/**output**)

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   readme
   contributing
   history
