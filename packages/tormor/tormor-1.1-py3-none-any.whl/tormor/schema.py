from tormor.connection import execute_sql_file, SchemaNotPresent
import os


MYDIR = os.path.dirname(os.path.abspath(__file__))

ADD_MODULE = """INSERT INTO module VALUES (%s)"""

BOOTSTRAP_SQL = """
CREATE TABLE module (
    name text NOT NULL,
    CONSTRAINT module_pk PRIMARY KEY(name)
);

CREATE TABLE migration (
    module_name text NOT NULL,
    CONSTRAINT migration_module_fkey
        FOREIGN KEY (module_name)
        REFERENCES module (name) MATCH SIMPLE
        ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE,
    migration text NOT NULL,
    CONSTRAINT migration_pk PRIMARY KEY (module_name, migration)
);
"""


class SchemaFilesNotFound(Exception):
    pass


def _get_schema_files_path():
    env_schema_path = os.getenv("SCHEMA_PATH")
    if env_schema_path:
        return env_schema_path.split(os.pathsep)
    return [os.path.join(MYDIR, "../../Schema")]


DEFAULT_SCHEMA_FILES_PATH = _get_schema_files_path()


def find_schema_path():
    """Searches the locations in the `SCHEMA_FILES_PATH` to
    try to find where the schema SQL files are located.
    """
    schema_files_path = DEFAULT_SCHEMA_FILES_PATH
    for path in schema_files_path:
        if os.path.isdir(path):
            return path
    raise SchemaFilesNotFound("Searched " + os.pathsep.join(schema_files_path))


def enablemodules(cnx, *modules):
    want = set(modules)
    try:
        got = cnx.load_modules()
    except SchemaNotPresent:
        cnx.pg.rollback()
        print("Tormor not loaded for this database. Bootstrapping...")
        cnx.execute(BOOTSTRAP_SQL)
        got = cnx.load_modules()
    for mod in want.difference(got):
        cnx.execute(ADD_MODULE, (mod,))
        print(mod, "enabled")
    cnx._modules = set()


def migrate(cnx):
    ## Find and execute all migration scripts that haven't already been run
    root = find_schema_path()
    scripts = []
    migrations = set(cnx.select("SELECT module_name, migration FROM migration"))
    for dirname, subdirs, files in os.walk(root):
        relpath = os.path.relpath(dirname, root)
        if relpath != "." and relpath in cnx.load_modules():
            scripts += [(relpath, f) for f in files if f.endswith(".sql")]
    scripts.sort(key=lambda m: m[1])
    for (mod, migration) in scripts:
        if (mod, migration) not in migrations:
            execute_sql_file(cnx, os.path.join(root, mod, migration))
