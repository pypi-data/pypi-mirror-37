import base64
import os
from datetime import datetime, timezone
from getpass import getpass

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_SERIALIZABLE

EPOCH = datetime(1970, 1, 1, tzinfo=timezone.utc)


class SchemaNotPresent(Exception):
    """Thrown if we can't load the list of modules because the `modules`
    table doesn't exist.
    """

    pass


class ModuleNotPresent(Exception):
    """ Thrown when a required module has not been installed.
    """

    pass


class Connection(object):
    def __init__(self, dsn):
        try:
            self.pg = psycopg2.connect(dsn)
        except psycopg2.OperationalError as e:
            if "fe_sendauth" in str(e):
                pwd = getpass()
                dsn = dsn + " password='%s'" % pwd
                self.pg = psycopg2.connect(dsn)
            else:
                raise e
        self.pg.set_session(isolation_level=ISOLATION_LEVEL_SERIALIZABLE)
        self.cursor = self.pg.cursor()
        self._modules = set()

    def load_modules(self):
        if not self._modules:
            try:
                self.cursor.execute("SELECT name FROM module")
                self._modules = set([m[0] for m in self.cursor.fetchall()])
            except psycopg2.ProgrammingError as e:
                if e.pgcode == "42P01":
                    raise SchemaNotPresent()
                else:
                    raise
        return self._modules

    def assert_module(self, module):
        """ Stops execution with an error if a required module is not installed
            in the system.
        """
        if not self.has_module(module):
            raise ModuleNotPresent(module)

    def has_module(self, module):
        """ Returns true if the module has been installed.
        """
        return module in self.load_modules()

    def execute(self, cmd, *args, **kwargs):
        """ Execute the SQL command and return the data rows as tuples
        """
        self.cursor.execute(cmd, *args, **kwargs)

    def select(self, cmd, *args, **kwargs):
        """ Execute the SQL command and return the data rows as tuples
        """
        self.cursor.execute(cmd, *args, **kwargs)
        return self.cursor.fetchall()

    def commit(self):
        self.pg.commit()


def execute_sql_file(cnx, filename):
    try:
        with open(filename) as f:
            cmds = f.read()
            cnx.cursor.execute(cmds)
        cnx.load_modules()
        print("Executed", filename)
    except Exception:
        print("Error whilst running", filename)
        raise


def execute_migration(cnx, module, migration, filename):
    try:
        with open(filename) as f:
            cmds = """
                INSERT INTO module (name) VALUES('{module}') ON CONFLICT (name) DO NOTHING;
                INSERT INTO migration (module_name, migration)  VALUES('{module}', '{migration}') ON CONFLICT (module_name, migration) DO NOTHING;    
                {cmds}
            """.format(
                module=module, migration=migration, cmds=f.read()
            )
            cnx.cursor.execute(cmds)
        cnx.load_modules()
        print("Executed", filename)
    except Exception:
        print("Error whilst running", filename)
        raise
