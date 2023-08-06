plotlog
=======

Output graph script by log file. In addition to a single file, you can
easily process a large number of identical format log files.

System requirements
-------------------

-  language : After Python 3.4.7
-  necessary package

   -  matplotlib
   -  pandas
   -  PyYAML

install
-------

.. code:: sh

    pip install plotlog

If you need build your environment

.. code:: sh

    git clone https://github.com/s-naoya/plotlog
    cd plotlog
    python setup.py install


Usage
-----

::

    plotlog [-h] [--setting SETTING_FILE_PATH] [--copy]
            [--new | --all | --after DATE | --select DATE [DATE ...] |
            --input LOG_FILE_PATH [LOG_FILE_PATH ...]] [--slice BEGIN END]
            [--noshift]

    optional arguments:
      -h, --help            show this help message and exit
      --setting SETTING_FILE_PATH
                            select setting file (default:'user.yml')
      --copy                copy original setting file
      --new                 DEFAULT: output graphs that has not been output yet
      --all                 output graphs for all data
      --after DATE          output graphs after the selected DATE(yyyymmddhhmm)
      --select DATE [DATE ...]
                            output graphs only selected DATEs
      --input LOG_FILE_PATH [LOG_FILE_PATH ...]
                            output graphs for selected log file
      --slice BEGIN END     sliced data by begin and end x-axis value
      --noshift             don't shift plot start time and x-axis

First, create setting file.

::

    plotlog --copy

Edit the created user.yml, setting each pass and the graph etc to
create. Setting items that do not need to be changed may be deleted.

Finish edit user.yml, create graph.

::

    plotlog

If user.yml is set correctly, a graph is drawn for a log file that has
not yet been output graph.

Setting
-------

It is reflected by editing user.yml. Also, this is reflected by creating
a new yaml file and reading it with the ``--setting`` argument.

Log file condition
------------------

-  Be sure to use the year, month, date, and time as the name of the log file and cam use some symbol.
   However, all log file names under put_log_dir must be in the same format.
   The format is specified by log_date_format in the configuration file.
-  Extension and separate character can change setting file.
-  All column equal all row
-  Put on the directory specified in the setting file (except when using
   –-input)

LICENCE
-------

This script is licenced under the MIT License. (See
`link <https://github.com/s-naoya/plotlog/blob/master/LICENSE>`__)
