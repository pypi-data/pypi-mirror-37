Instructions for data users
===========================

Data users are scientists analysing data from the data pool.


All data is store in a PostgrSQL database so that arbitrary queries
can be performed. The figure below shows the
database layout.

.. image:: ./graphics/DataModel.svg



Connect to data pool
--------------------

To connect with the database you need the following information from your admin:

- The host, e.g. "a.server.com"
- The port of the database, e.g. 5432
- The name of the database, e.g. "datapool"
- A database user name, e.g "data_user"
- The database password

You can connect directly to the database via `psql <http://postgresguide.com/utilities/psql.html>`_.
However, it is more convenient to load the data required directly in
the environment used for further analysis:

R
~

With the `RPostgreSQL package <https://cran.r-project.org/web/packages/RPostgreSQL/>`_ data can be
loaded directly into R.

However, for *Eawag internal* usage the
`DatapoolR package <https://eaw-test-gitlab.eawag.wroot.emp-eaw.ch/scheidan/DatapoolR>`_
should be preferred. It connects automatically to the database and
provides convenient helper functions.


Python
~~~~~~

Different options exist, `psycopg2 <https://wiki.postgresql.org/wiki/Using_psycopg2_with_PostgreSQL>`_ is widly used.


Example SQL queries
-------------------

The SQL language may look cumbersome at first. However, it gives a lot of flexibility and allows to express even very complex queries. This `SQL tutorial <https://www.w3schools.com/sql/default.asp>`_ is a helpful reference.

Also note that the `DatapoolR package <https://eaw-test-gitlab.eawag.wroot.emp-eaw.ch/scheidan/DatapoolR>`_ provides functions to simplify common queries.



List all data sources:

.. code-block:: sql

		SELECT srctype.name, src.name, src.serial, srctype.description, src.description
		FROM source_type AS srctype, source AS src
		WHERE src.source_type_id = srctype.source_type_id;


List all sites and check how many images a site has:

.. code-block:: sql

		SELECT name, coord_x, coord_y, coord_z, street,
		  postcode, COUNT(picture.filename), site.description
		FROM site
		  LEFT JOIN picture ON site.site_id=picture.site_id
		GROUP BY site.site_id;

Get all signals measured at site ``site_A`` within a given time interval:

.. code-block:: sql

		SELECT signal.timestamp, value, unit, parameter.name, source_type.name, source.name
		FROM signal
		  INNER JOIN site ON signal.site_id = site.site_id
		  INNER JOIN parameter ON signal.parameter_id = parameter.parameter_id
		  INNER JOIN source ON signal.source_id = source.source_id
		  INNER JOIN source_type ON source.source_type_id = source_type.source_type_id
		WHERE site.name = site_A AND
		  ?tmin::timestamp <= "2017-01-01 00:12:00"::timestamp AND
		  signal.timestamp <= "2017-01-01 00:18:00"::timestamp;
