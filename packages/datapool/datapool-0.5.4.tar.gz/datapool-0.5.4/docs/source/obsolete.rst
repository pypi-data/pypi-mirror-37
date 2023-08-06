Obsolete documentation
======================

This material should be worked in to the other sections.


Run server in test mode
-----------------------

The following sequence initializes  ``datapool`` and runs the server in single
process mode.

.. code-block:: bash

    $ rm -rf ./lz 2>/dev/null

    $ export ETC=./etc
    $ rm -rf $ETC 2>/dev/null

    $ pool init-config --use-sqlitedb ./lz
    $ pool init-db
    $ pool check-config
    $ pool run-simple-server


Usually ``pool init-config`` would write to ``/etc/datapool`` and thus the
command requires ``root`` privileges. Setting the environment variable ``ETC``
allows overriding the ``/etc`` folder so we do not interfere with a global
setup.

Further we use ``--use-sqlitedb`` so configuration and setup of a data base
system as Postgres is not required. This flag is introduced for testing, in
operational mode we recommond to avoid this flag and configer  Postgres
instead.

The last ``run-simple-server`` command will observe changes to the operational
landing zone at `./lz`  and report its operations. The command does not run in
the background and thus will block the terminal until the user presses ``CTRL-C``
to enforce shutdown.

As a data provider we open another terminal window, setup a development landing
zone and commit the defaults to the operational landing zone. You should then
see some output from the ``run-simple-server`` command in the previous terminal
window:

.. code-block:: bash

    $ rm -rf ./dlz 2>/dev/null
    $ export ETC=./etc

    $ pool start-develop dlz
    $ pool check dlz
    $ pool update-operational dlz




Workflow example
----------------

To initialize ``datapool`` configuration on the current server run the ``init-config`` subcommand,
this might require admin permissions because the config file is stored in the ``/etc/datapool``
folder:

.. code-block:: bash

	$ pool init-config ./lz

	> init-config
	- guess settings
	  - 'matlab' not found on $PATH
	- created config files at /etc/datapool
	  please edit these files and adapt the data base configuration to your setup
	+ initialized landing zone at ./lz


Then edit this file and run ``pool check-config``:

.. code-block:: bash

	$ pool check-config

	> check-config
	- check settings in config file /etc/datapool/datapool.ini
	- try to connect to db
	- could not connect to db postgresql://user:password@localhost:5432/datapool
	- check R configuration + code execution
	- matlab not configured, skip tests
	- check julia configuration + code execution
	- check julia version.
	- check python configuration + code execution
	+ all checks passed


To start development create a so called *development landing zone** which can be an
arbitrary folder:

.. code-block:: bash

	$ pool start-develop ./dlz

	> start-develop
	- setup development landing zone
	- operational landing zone is empty. create development landing zone with example files.
	+ setup done


This copied some example ``.yaml`` files, conversion scripts and raw data files. To check
the scripts run:

.. code-block:: bash

	$ pool check-scripts ./dlz

	> check-scripts
	- check landing zone at ./dlz
	- check ./dlz/data/sensor_from_company_xyz/sensor_instance_julia/conversion.jl
	- wrote conversion result to /tmp/tmp9hcxslxv/sensor_instance_julia_0.csv
	- wrote conversion result to /tmp/tmp9hcxslxv/sensor_instance_julia_0.txt
	- check ./dlz/data/sensor_from_company_xyz/sensor_instance_python/conversion.py
	- wrote conversion result to /tmp/tmp9hcxslxv/sensor_instance_python_0.csv
	- wrote conversion result to /tmp/tmp9hcxslxv/sensor_instance_python_0.txt
	- check ./dlz/data/sensor_from_company_xyz/sensor_instance_r/conversion.r
	- wrote conversion result to /tmp/tmp9hcxslxv/sensor_instance_r_0.csv
	- wrote conversion result to /tmp/tmp9hcxslxv/sensor_instance_r_0.txt
	+ congratulations: checks succeeded.

This checked the scripts and you can inspect the results files as displayed in the output.

To check the ``.yaml`` files:

.. code-block:: bash

	$ pool check-yamls ./dlz/

	> check-yamls
	- check yamls in landing zone at ./dlz/
	- setup fresh development db. productive does not exist or is empty.
	- load and check 1 new yaml files:
	- ./dlz/data/parameters.yaml
	+ all yaml files checked

Now you can upload the changes from the development landing zone to the operational
landing zone:

.. code-block:: bash

	$ pool update-operational ./dlz

	> update-operational
	- check before copying files around.
	- copied data/parameters.yaml
	- copied data/sensor_from_company_xyz/sensor_instance_julia/conversion.jl
	- copied data/sensor_from_company_xyz/sensor_instance_julia/raw_data/data-001.raw
	- copied data/sensor_from_company_xyz/sensor_instance_matlab/raw_data/data-001.raw
	- copied data/sensor_from_company_xyz/sensor_instance_python/conversion.py
	- copied data/sensor_from_company_xyz/sensor_instance_python/raw_data/data-001.raw
	- copied data/sensor_from_company_xyz/sensor_instance_r/conversion.r
	- copied data/sensor_from_company_xyz/sensor_instance_r/raw_data/data-001.raw
	- copied data/sensor_from_company_xyz/source_type.yaml
	- copied sites/example_site/images/24G35_regenwetter.jpg
	- copied sites/example_site/images/IMG_0312.JPG
	- copied sites/example_site/images/IMG_0732.JPG
	- copied sites/example_site/site.yaml
	+ copied 13 files to ./lz
