# Tormor command line tool

    $ tormor -?
    Manage an Tormor database

        SCHEMA_PATH=/usr/src/Schema tormor [opts] command [args]

    ...


The `enable-modules` and `migrate` commands are used for managing the Tormor installation.


### Run script in another filename

    include filename

Find commands (one per line) in the specified file and run them


### Run a SQL script

    sql filename

Load the filename and present the SQL in it to the database for execution. This is useful for choosing migrations scripts to run.

