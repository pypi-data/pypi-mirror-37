Instructions for data provider
==============================

Data provider is usually the scientist performing measurements in the field.


System Architecture
-------------------

Data flow model :download:`specification <../graphics/DataFlowModel.svg>`.


.. image:: ./../graphics/DataFlowModel.svg

The data provider must make sure that i) the raw data arrive in the
landing-zone at the right place, ii) a conversions script exist to
standardize the raw data, and iii) meta-data are provided.


General workflow
----------------

Working on the real landing-zone would be dangerous. Therefore, all
development and testing is done on a copy of the
landing-zone. The datapool provides a command to create development
landing-zones. A development landing-zone can have any names, but let's call it
``dlz`` for now:

.. code-block:: none

    $ pool start-develop dlz

This creates a folder (a copy of the real landing-zone) called ``dlz`` in the home directory. You can
see how the created landing zone looks like with ``ls -l dlz``.

The datapool provides various checks to ensure that the provided
conversion scripts and meta-data are consistent. The checks are ran by:

.. code-block:: none

    $ pool check dlz


If everything is fine, modify the develop landing-zone (e.g. add a new
sensor) according to the instructions given below. After the
modifications run the checks again.

.. code-block:: none

    $ pool check dlz


It is recommended to execute this checks after any small changes. If this succeeds, update the operational landing zone:

.. code-block:: none

    $ pool update-operational dlz

All future raw data should be delivered directly into the operational database.


In the following sections, the different types of modifications/additions are
explained.



Add Raw Data to Existing Source
--------------------------------


Raw data files are written to the respective ``data/`` folders in the
operational landing zone as follows:

1. A new file, for example ``data.incomplete``, is created and data are written to this
   file.

2. Once the file content is complete and the corresponding file handle is
   closed, the file is renamed to ``data-TIMESTAMP.raw``.

*Note, the file must end with ``.raw``!
The actual format of ``TIMESTAMP`` is not fixed but must be unique string,
that starts with a dash ``-``, and can be temporarily ordered. Encoding a full date and time string
will help the users and developers to inspect and find files, especially
if present in the backup zone.

This procedure is called *write-rename pattern* and avoids conversion of
incomplete data files. The risk for such a race condition depends on the
size of the incoming data files and other factors and is probably very
low. But running a data pool over a longer time span increases this risk
and could result in missing data in the data base.




Add Site
--------

In order to add a new measuring site, the information about this site have to be provided as a ``site.yaml`` file in a new folder for the site, within the ``sites`` folder of the landingzone. The information to be specified are:

- Name: Name of the site

- Description: Free Text describing the particularities of the site

- Street, City and Coordinates (CH1903/LV03): Specifying where the site is located

- Pictures (optional): Pictures relating to the site can be specified. Pictures are normally stored in the ``images`` folder of the specific site.

The structure of the file has to be the same as in the example below:

.. include:: site_example.rst



Add or Modify Parameters
------------------------

The file ``parameters.yaml`` is stored in the ``data`` folder and contains all the parameters. New parameters can be added here. The information to be included are:

- Name: Name of the Parameter

- Unit: Specifies the unit of the Parameter

- Description: Additional description of the parameter. In case there is no description required, the field can remain empty.

The syntax has to match the following example (note the dash in the first line):

.. code-block:: YAML

    -
       name: Absorbance 202.50_nm
       unit: m-1
       description: absorbance at 202.50 nm wavelength


Add a new Source Type
---------------------
TODOXS


Add Source Instance
-------------------
todo

Conversion of raw data
~~~~~~~~~~~~~~~~~~~~~~

The files arriving in the landing zone are called *raw data*. Every
raw data file must be converted into a so called *standardized file* by
a conversion script. The format of the standardized files is defined
below. Typically, every source instance needs an individually adapted
conversion script.

Standardized file format
~~~~~~~~~~~~~~~~~~~~~~~~

The standardized file format for the input data is a ``csv`` file with
either six or four columns. It must adhere the following standards:


- File format: ``csv`` file with semicolon delimited (``;``)

- Data format: ``yyyy-mm-dd hh:mm:ss``

- Column names: The first row contains the column names. The first
  three are always: ``timestamp``, ``parameter``, ``value``. Next
  either the three columns ``x``, ``y``, ``z``, or a single column
  ``site`` must be given. The parameter must exisit in the
  ``parameters.yaml`` and have the exactly same name (see above).

- ``value`` column: Must contain only numerical values. Missing values
  (``NULL``, ``NA``, or similar) are not allowed.

- The z-coordinate columns may be empty.


Example standardized file format with coordinates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


+---------------------+-----------------------+--------+--------+--------+-----+
| timestamp           | parameter             | value  | x      | y      | z   |
+=====================+=======================+========+========+========+=====+
| 2013-11-13 10:06:00 | Water Level           | 148.02 | 682558 | 239404 |     |
+---------------------+-----------------------+--------+--------+--------+-----+
| 2013-11-13 10:08:00 | Water Level           | 146.28 | 682558 | 239404 |     |
+---------------------+-----------------------+--------+--------+--------+-----+
| 2013-11-13 10:08:00 | Average Flow Velocity | 0.64   | 682558 | 239404 | 412 |
+---------------------+-----------------------+--------+--------+--------+-----+
| ...                 | ...                   | ...    | ...    | ...    |     |
+---------------------+-----------------------+--------+--------+--------+-----+

Example standardized file format with site
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

+---------------------+-----------------------+--------+--------+
| timestamp           | parameter             | value  | site   |
+=====================+=======================+========+========+
| 2013-11-13 10:06:00 | Water Level           | 148.02 | zurich |
+---------------------+-----------------------+--------+--------+
| 2013-11-13 10:08:00 | Water Level           | 146.28 | zurich |
+---------------------+-----------------------+--------+--------+
| 2013-11-13 10:08:00 | Average Flow Velocity | 0.64   | zurich |
+---------------------+-----------------------+--------+--------+
| ...                 | ...                   | ...    | ...    |
+---------------------+-----------------------+--------+--------+


Conversion script
~~~~~~~~~~~~~~~~~

The conversion script must define a *function* which reads raw data and write an output
file (a standardized file). The first argument if this function is the
path to the input raw data, the second argument the path to the resulting file.

The follwing points should be considered when writing an conversion script:

- Indicate corrupt input data by throwing an exception
  within a conversion script. A informative error message is helpful and will be logged.

- If a converson script writes to ``stdout`` (i.e. normal ``print()``
  commands) this may not appear in the datapool log file and thus
  might be overseen.

- All required third party modules, packages, or libraries must be
  installed globally. Do not try to install them within a script.


The following code snippets show how a conversion script
could look like for different languages.

R
~
- The file must be named ``conversion.r``.
- The function must be named ``convert``.

.. include:: r_example.rst

Julia
~~~~~

- The function must be named ``convert``.
- The name of the julia file and the declared module must be the same (up to
  the ``.jl`` file extension). So the file containing the module
  ``conversion_lake_zurich`` must be saved as ``conversion_lake_zurich.jl``.
- Further the module and file name must be unique within the landing zone.

.. include:: julia_example.rst


Python
~~~~~~

.. include:: python_example.rst

Matlab
~~~~~~

- The function must be named ``convert``.
- The file name must be named ``convert.m``.


.. include:: matlab_example.rst
