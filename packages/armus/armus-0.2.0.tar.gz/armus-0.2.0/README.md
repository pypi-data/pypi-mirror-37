
[![Circle CI](https://circleci.com/gh/ustudio/armus.svg?style=svg&circle-token=9f77bab2ae75ccdbefe30a7b0551a8fc52e53cac)](https://circleci.com/gh/ustudio/armus)

Standalone Migration Tool a.k.a. "Armus"
=================

<img src="http://vignette1.wikia.nocookie.net/memoryalpha/images/5/58/Armus.jpg/revision/latest?cb=20120728222622&path-prefix=en" width="150"
 alt="armus logo" title="armus" align="right" />

### What is Armus?

Armus is an open source tool for running migration scripts.  It was developed in an effort to simplify database migrations at [uStudio](http://www.ustudio.com).



### Create Migration

Armus includes a script to generate a migration module and associated test.

#### Command Line Usage

-p path to migrations *(defaults to "migrations")*

-d description of migration i.e. add_field_to_user_table

If the migration and testing directories do not exist they will be created for you.

ex. ```python armus/bin/create_migration.py -d MIGRATION_DESCRIPTION ```

### Apply migrations

The migrations.py module handles executing your migration scripts.

ex.
```
from armus import migrations

migrations.apply_new(PATH_TO_MIGRATIONS_PACKAGE, LIST_OF_APPLIED_MIGRATIONS, **kwargs)

```

### Revert last

## TO DO

1. Make create-migration an easily executable script (i.e. armus create-migration --params)
