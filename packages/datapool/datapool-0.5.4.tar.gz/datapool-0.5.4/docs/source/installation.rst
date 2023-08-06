Instructions for Admin
======================

Installation on Ubuntu 16.04
----------------------------


Run the following instructions as ``root`` (this means, type ``sudo`` in front of every command) in order to have the root rights.
If a file needs to be opened/modified, use the editor "nano" (type ``nano`` in front of the filename).


 1. Ubuntu packages

    .. code-block:: none

       $ apt install git r-base postgresql python3-pip python3-psycopg2


 2. Install julia 0.5.1 and create a symbolic link: (Ubuntu offers julia 0.4.x only):

    .. code-block:: none

        $ wget https://julialang.s3.amazonaws.com/bin/linux/x64/0.5/julia-0.5.1-linux-x86_64.tar.gz
        $ tar xzf julia-0.5.1-linux-x86_64.tar.gz
        $ mv julia-6445c82d00 /opt
        $ ln -s /opt/julia-6445c82d00/bin/julia /usr/local/bin/
        $ julia --version


 3.  Create data base users and database

    We create a user ``datapool`` who owns the ``datapool`` database and thus has all permissions to modify
    tables and data in this database. In addition to that we create a ``datapool_reader`` user which only
    has read access.

    .. code-block:: none

        $ sudo -u postgres createuser -P datapool
        $ sudo -u postgres createuser -P datapool_reader

    Note down the choosen passwords for both users.

    Then create the database and restrict the pemissions of ``datapool_reader``.

    .. code-block:: none

        $ sudo -u postgres createdb -O datapool datapool
        $ sudo -u postgres psql -c "REVOKE ALL PRIVILEGES ON ALL TABLES IN SCHEMA public FROM datapool_reader;"
        $ sudo -u postgres psql -c "GRANT SELECT ON ALL TABLES IN SCHEMA public TO datapool_reader;"

    Now check:

    .. code-block:: none

        $ psql -U datapool -h 127.0.0.1 datapool
        $ ^D    (control-D to exit postgress shell)

    Next, the database must be configured to allow for remote
    access.

    In the file ``/etc/postgresql/9.5/main/pg_hba.conf`` edit the line
    ``host    all             all             127.0.0.1/32              md5``
    to
    ``host    all             all             0.0.0.0/0                 md5``
    .

    In the file ``/etc/postgresql/9.5/main/postgresql.conf`` change
    ``listen_addresses = 'localhost'`` to ``listen_addresses = '*'``.

    Restart the data base:

    .. code-block:: none

        $ service postgresql restart

 4. Install datapoool

    .. code-block:: none

        $ cd /opt
        $ git clone https://sissource.ethz.ch/sispub/eawag_datapool.git
        $ pip3 install -e eawag_datapool


    Check installation:

    .. code-block:: none

        $ pool --help


    Install needed packages for demo scripts:

    .. code-block:: none

        $ /opt/eawag_datapool/scripts/setup_julia.sh
        $ /opt/eawag_datapool/scripts/setup_python.sh
        $ /opt/eawag_datapool/scripts/setup_r.sh


 5. Create user account for data provider:

    .. code-block:: none

        $ addgroup datapool
        $ useradd -m -G datapool,systemd-journal -s /bin/bash datapool-provider


    Assign password:

    .. code-block:: none

        $ passwd datapool-provider



 6. Initalize datapool configuration and setup landing zone:

    We assume that the landing zone will be located on a shared drive mounted at ``/nfsmount``,
    but you are free to choose any other folder.


    Create the landing zone and link it to the data pool:

    .. code-block:: none

        $ mkdir -p /nfsmount/landing_zone
        $ pool init-config /nfsmount/landing_zone

    Set the correct permissions:

    .. code-block:: none

        $ chgrp -R datapool /nfsmount/landing_zone
        $ chmod -R g+w /nfsmount/landing_zone


 7. Adapt configuration:

    .. code-block:: none

        $ /etc/datapool/datapool.ini


    Add the database user and password. Replace ``DB_USER`` and
    ``DB_PASSWORD`` with the one selsceted in step 3.

    .. code-block:: none

        ...
        [db]
        connection_string = postgresql://DB_USER:DB_PASSWORD@127.0.0.1:5432/datapool


    If necessary adapt also the path to the landing zone, define a
    backup landingzone, or change software versions.


    Then check:

    .. code-block:: none

        $ pool check-config


 8.  Create the central management tool service for controlling the init system:

    .. code-block:: none

        $ ln -s /opt/eawag_datapool/scripts/datapool.service /etc/systemd/system
        $ systemctl daemon-reload


 9.  Start service:

    .. code-block:: none

        $ systemctl start datapool.service
        $ systemctl status datapool.service


 10.  Observe running service:

    can be stopped with ^C), can be used without ``-f``:

    .. code-block:: none

        $ journalctl -u datapool -f

    Keep this terminal window open if you want observe the datapool activities.

 11. Install julia packages:

    Login as user ``datapool-provider`` first.

    Install needed Julia packages (these are installed per user) to be
    able to run the test scripts:

    .. code-block:: none

        $ /opt/eawag_datapool/scripts/setup_julia.sh
