gabra_converter
===============

Requirements:

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

.. toctree::
    :maxdepth: 1

    gabra_converter/converters
