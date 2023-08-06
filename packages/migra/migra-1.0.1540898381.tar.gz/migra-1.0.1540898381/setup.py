# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['migra']

package_data = \
{'': ['*']}

install_requires = \
['schemainspect', 'six', 'sqlbag']

extras_require = \
{'pg': ['psycopg2-binary']}

entry_points = \
{'console_scripts': ['migra = migra:do_command']}

setup_kwargs = {
    'name': 'migra',
    'version': '1.0.1540898381',
    'description': 'Like `diff` but for PostgreSQL schemas',
    'long_description': '# migra: PostgreSQL migrations made almost painless\n\n`migra` is a schema diff tool for PostgreSQL. Use it to compare database schemas or autogenerate migration scripts. Use it in your python scripts, or from the command line like this:\n\n    $ migra postgresql:///a postgresql:///b\n    alter table "public"."products" add column newcolumn text;\n\n    alter table "public"."products" add constraint "x" CHECK ((price > (0)::numeric));\n\n`migra` magically figures out all the statements required to get from A to B.\n\nYou can also detect changes for a single specific schema only with `--schema myschema`.\n\n## Folks, schemas are good\n\nSchema migrations are without doubt the most cumbersome and annoying part of working with SQL databases. So much so that some people think that schemas themselves are bad!\n\nBut schemas are actually good. Enforcing data consistency and structure is a good thing. It’s the migration tooling that is bad, because it’s harder to use than it should be. ``migra`` is an attempt to change that, and make migrations easy, safe, and reliable instead of something to dread.\n\n**Migra supports PostgreSQL >= 9.4.** Known issues exist with earlier versions.\n\n## Full documentation\n\nDocumentation is at [migra.djrobstep.com](https://migra.djrobstep.com).\n\n## How it Works\n\nThink of `migra` as a diff tool for schemas. Suppose database A and database B have similar but slightly different schemas. `migra` will detect the differences and output the SQL needed to transform A to B.\n\nThis includes changes to tables, views, functions, indexes, constraints, enums, sequences, and installed extensions.\n\nYou can also use `migra` as a library to build your own migration scripts, tools, and custom migration flows.\n\nWith migra, a typical database migration is a simple three step process.\n\n1. Autogenerate:\n\n        $ migra --unsafe postgresql:///a postgresql:///b > migration_script.sql\n\n2. Review (and tweak if necessary).\n\n        # If you need to move data about during your script, you can add those changes to your script.\n\n3. Apply:\n\n        $ psql a --single-transaction -f migration_script.sql\n\nMigration complete!\n\n## IMPORTANT: Practice safe migrations\n\n**Migrations can never be fully automatic**. As noted above **ALWAYS REVIEW MIGRATION SCRIPTS CAREFULLY, ESPECIALLY WHEN DROPPING TABLES IS INVOLVED**.\n\nMigra manages schema changes **but not your data**. If you need to move data around, as part of a migration, you\'ll need to handle that by editing the script or doing it separately before/after the schema changes.\n\nBest practice is to run your migrations against a copy of your production database first. This helps verify correctness and spot any performance issues before they cause interruptions and downtime on your production database.\n\n`migra` will deliberately throw an error if any generated statements feature the word "drop". This safety feature is by no means idiot-proof, but might prevent a few obvious blunders.\n\nIf you want to generate "drop ..." statements, you need to use the `--unsafe` flag if using the command, or if using the python package directly, `set_safety(` to false on your `Migration` object.\n\n## Python Code\n\nHere\'s how the migra command is implemented under the hood (with a few irrelevant lines removed).\n\nAs you can see, it\'s pretty simple (`S` here is a context manager that creates a database session from a database URL).\n\n    from migra import Migration\n    from sqlbag import S\n\n    with S(args.dburl_from) as s0, S(args.dburl_target) as s1:\n        m = Migration(s0, s1)\n\n        if args.unsafe:\n            m.set_safety(False)\n\n        m.add_all_changes()\n        print(m.sql)\n\nHere the code just opens connections to both databases for the Migration object to analyse. `m.add_all_changes()` generates the SQL statements for the changes required, and adds to the migration object\'s list of pending changes. The necessary SQL is now available as a property.\n\n## Features and Limitations\n\n`migra` plays nicely with extensions. Schema contents belonging to extensions will be ignored and left to the extension to manage.\n\n**New:** `migra` now plays nicely with view dependencies too, and will drop/create them in the correct order.\n\nOnly SQL/PLPGSQL functions are confirmed to work so far. `migra` ignores functions that use other languages.\n\n## Installation\n\nAssuming you have [pip](https://pip.pypa.io), all you need to do is install as follows:\n\n    $ pip install migra\n\nIf you don\'t have psycopg2-binary (the PostgreSQL driver) installed yet, you can install this at the same time with:\n\n    $ pip install migra[pg]\n\n## Contributing\n\nContributing is easy. [Jump into the issues](https://github.com/djrobstep/migra/issues), find a feature or fix you\'d like to work on, and get involved. Or create a new issue and suggest something completely different. Beginner-friendly issues are tagged "good first issue", and if you\'re unsure about any aspect of the process, just ask.\n\n## Credits\n\n- [https://github.com/djrobstep](djrobstep): initial development, maintenance\n- [https://github.com/alvarogzp](alvarogzp): privileges support\n- [https://github.com/seblucas](seblucas): docker improvements\n- [https://github.com/MOZGIII](MOZGIII): docker support\n\n\n\n',
    'author': 'Robert Lechte',
    'author_email': 'robertlechte@gmail.com',
    'url': 'https://migra.djrobstep.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
}


setup(**setup_kwargs)
