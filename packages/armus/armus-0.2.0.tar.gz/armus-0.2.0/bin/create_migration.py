#!/usr/bin/python
"""Create migration and associated test file from template"""

import optparse
import os
from datetime import datetime
import logging

DEFAULT_MIGRATION_PATH = "migrations"
VERSION_FORMAT = "%Y%m%d%H%M%S"
MIGRATION_TEMPLATE = """
def up():
    pass


def down():
    pass
"""

MIGRATION_TEST_TEMPLATE = """
\"\"\"(Write a doc string).\"\"\"
import unittest
from migrations import {0}


class TestMigration(unittest.TestCase):
    def test_new_migration(self):
        migration = {0}

        migration.up()
        migration.down()

        self.assertTrue(False, "Migration test has not been written yet.")
"""


def main():
    logging.basicConfig(
        format="%(asctime)s %(levelname)s:%(module)s:%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S%z", level=logging.INFO)

    parser = optparse.OptionParser(description="Run data migrations.")
    parser.add_option(
        "-p", "--path", dest="path", default=DEFAULT_MIGRATION_PATH,
        help="Path to the migrations.")
    parser.add_option(
        "-n", "--new-migration", dest="new_migration", default=False,
        help="Create new migration and test file", action="store_true")
    parser.add_option(
        "-d", "--description", dest="description", default="new_migration",
        help="Description of the migration to generate.")
    opts, args = parser.parse_args()

    _generate_migration(opts.path, opts.description, opts.new_migration)


def _generate_migration(path, description, new_migration):

    version = datetime.today().strftime("%Y%m%d%H%M%S")
    base_name = "migration_{0}_{1}".format(version, description.lower())
    name = "{0}/{1}.py".format(path, base_name)
    test_path = os.path.abspath(os.path.join(path, '..', 'tests'))

    test_name = "{0}/migrations/test_{1}.py".format(test_path, base_name)

    if os.path.isdir(os.path.join(path)) is False:
        os.mkdir(os.path.join(path))

    if os.path.isdir(os.path.join(test_path, path)) is False:
        os.mkdir(os.path.join(test_path, path))

    if new_migration:
        with open(name, "w") as migration_file:
            migration_file.write(MIGRATION_TEMPLATE)
            logging.info(" ".join(("Migration:\n", name, "created!")))

        with open(test_name, "w") as migration_file:
            migration_file.write(MIGRATION_TEST_TEMPLATE.format(base_name))
            logging.info(" ".join(("Test:\n", test_name, "created!")))


if __name__ == "__main__":
    main()
