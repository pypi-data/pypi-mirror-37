import csv
from tormor.connection import execute_sql_file, Connection, SchemaNotPresent
from tormor.schema import enablemodules, migrate
from psycopg2 import ProgrammingError
import os
import sys
from getopt import gnu_getopt


SHORTOPTS = "?d:h:p:U:P:"
PGOPTMAP = {
    "-d": ("dbname", "PGDATABASE"), 
    "-h": ("host", "PGHOST"), 
    "-p": ("port", "PGPORT"), 
    "-U": ("user", "PGUSER"),
    "-P": ("password", "PGPASSWORD")
}

HELPTEXT = """Tormor -- Migration management

    tormor [opts] command [args]

opts are one or more of:

    -?                      Print this text
    -h hostname             Postgres host
    -d database             Database name
    -U username             Database username (role)
    -p port                 Database port
    -P password             Database password (Not recommended, use environment variable PGPASSWORD instead)

Command is one of:
    enable-modules mod1 [mod2 [mod3 ...]]
        Enable the modules.

    help
        Show this text

    include filename
        Find commands (one per line) in the specified file and run them

    migrate
        Run all migrations.

    sql filename
        Load the filename and present the SQL in it to the database for
        execution. This is useful for choosing migrations scripts to run.

"""


def makedsn(opts, args):
    dsnargs = {}
    for arg, (opt, env) in PGOPTMAP.items():
        if arg in opts:
            dsnargs[opt] = opts[arg]
        elif os.getenv(env):
            dsnargs[opt] = os.getenv(env)
    return " ".join(["%s='%s'" % (n, v) for n, v in dsnargs.items()])


def include(cnx, filename):
    with open(filename, newline="") as f:
        lines = csv.reader(f, delimiter=" ")
        for line in lines:
            if len(line) and not line[0].startswith("#"):
                command(cnx, *[p for p in line if p])


COMMANDS = {
    "enable-modules": enablemodules,
    "migrate": migrate,
    "include": include,
    "sql": execute_sql_file,
}


class UnknownCommand(Exception):
    pass


def command(cnx, cmd, *args):
    if cmd in COMMANDS:
        COMMANDS[cmd](cnx, *args)
    else:
        raise UnknownCommand(cmd)

def script():
    optlist, args = gnu_getopt(sys.argv, SHORTOPTS)
    opts = dict(optlist)

    if len(args) < 2:
        print("No command given. Type 'tormor help' for help")
        exit(3)
    elif '-?' in opts or args[1] == 'help':
        print(HELPTEXT)
    else:
        try:
            dsn = makedsn(opts, args)
            cnx = Connection(dsn)
            command(cnx, *(args[1:]))
            cnx.commit()
        except UnknownCommand as e:
            print("Unknown command '{}'. Type 'tormor help' for help".format(e))
            exit(1)
        except ProgrammingError as e:
            print("** Postgres error", e.pgcode)
            print()
            print(e)
            exit(2)
        except SchemaNotPresent:
            print("This database does not have the Tormor schemas installed")
            print("Use `tormor enable-modules` to bootstrap it")
            exit(3)
