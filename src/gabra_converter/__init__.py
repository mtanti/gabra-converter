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

----

Packages:
'''

import os

__version__ = '0.0.0'

path = os.path.dirname(os.path.abspath(__file__))
