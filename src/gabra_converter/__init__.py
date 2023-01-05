'''
Feature requirements:

.. list-table::
   :header-rows: 1

   * - Requirement ID
     - Description

   * - ``archive_extractor``
     - The program should extract the JSON lines files of the lexemes
       and wordforms collections from the database dump.

   * - ``data_loader``
     - The program should load the JSON encoded Mongo documents according
       to the schema in https://mlrs.research.um.edu.mt/resources/gabra-api/p/schema
       and any divergent documents should be fixed if possible or skipped
       if unfixable.

   * - ``export``
     - The program should be able to export lexeme and wordform rows
       into readable file formats such as CSV, with field containing
       lists being exported to separate files with foreign keys in order
       to efficiently store the one-to-many relationships.

----

Packages:
'''

import os

__version__ = '0.0.0'

path = os.path.dirname(os.path.abspath(__file__))
