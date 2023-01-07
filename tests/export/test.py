'''
Test the export requirement.
'''

import os
import tempfile
import unittest
import json
import gabra_converter
from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow
from gabra_converter.converters.lexemes.exporters.lexeme_exporter_list import (
    get_all_lexeme_exporters
)
from gabra_converter.converters.lexemes.cleaners.lexeme_cleaner_list import (
    get_all_lexeme_cleaners
)
from gabra_converter.converters.wordforms.row.wordform_row import WordformRow
from gabra_converter.converters.wordforms.exporters.wordform_exporter_list import (
    get_all_wordform_exporters
)
from gabra_converter.converters.wordforms.cleaners.wordform_cleaner_list import (
    get_all_wordform_cleaners
)


#########################################
class Test(unittest.TestCase):
    '''
    As described.
    '''

    #########################################
    def test_unique_ids(
        self,
    ) -> None:
        '''
        Test that the IDs in the lexeme exporter list and in the wordform exporter list are unique.
        '''
        self.assertCountEqual(
            list({exporter.id_ for exporter in get_all_lexeme_exporters()}),
            [exporter.id_ for exporter in get_all_lexeme_exporters()],
            msg='lexeme exporters',
        )
        self.assertCountEqual(
            list({exporter.id_ for exporter in get_all_wordform_exporters()}),
            [exporter.id_ for exporter in get_all_wordform_exporters()],
            msg='wordform exporters',
        )

    #########################################
    def test_lexemes_wordforms_equal_ids(
        self,
    ) -> None:
        '''
        Test that the lexeme exporter list and the wordforms exporter list both have
        the same IDs.
        '''
        self.assertEqual(
            {exporter.id_ for exporter in get_all_lexeme_exporters()},
            {exporter.id_ for exporter in get_all_wordform_exporters()},
        )

    #########################################
    def test_required_cleaners(
        self,
    ) -> None:
        '''
        Check that all the cleaner IDs mentioned in the required_cleaners instance variable are
        existing ones.
        '''
        cleaner_ids = {cleaner.id_ for cleaner in get_all_lexeme_cleaners()}
        for exporter in get_all_lexeme_exporters():
            for required_id in exporter.required_cleaners:
                self.assertIn(required_id, cleaner_ids, msg=f'lexeme exporter {exporter.id_}')

        cleaner_ids = {cleaner.id_ for cleaner in get_all_wordform_cleaners()}
        for exporter in get_all_wordform_exporters():
            for required_id in exporter.required_cleaners:
                self.assertIn(required_id, cleaner_ids, msg=f'wordform exporter {exporter.id_}')

    #########################################
    def test_csv(
        self,
    ) -> None:
        '''
        Test the CSV exporters.
        '''
        with tempfile.TemporaryDirectory() as tmp_path:
            lexeme_exporters = [
                exporter for exporter in get_all_lexeme_exporters()
                if exporter.id_ == 'csv'
            ]
            self.assertEqual(len(lexeme_exporters), 1)
            lexeme_exporter = lexeme_exporters[0]

            lexeme_exporter.create(tmp_path)
            with open(
                os.path.join(
                    gabra_converter.path, '..', '..', 'tests', 'export', 'test_input',
                    'lexemes.jsonl'
                ),
                'r', encoding='utf-8'
            ) as f:
                for line in f:
                    lexeme_exporter.add_row(LexemeRow(**json.loads(line.strip())))
            lexeme_ids = lexeme_exporter.get_id_map()

            wordform_exporters = [
                exporter for exporter in get_all_wordform_exporters()
                if exporter.id_ == 'csv'
            ]
            self.assertEqual(len(wordform_exporters), 1)
            wordform_exporter = wordform_exporters[0]

            wordform_exporter.create(tmp_path)
            with open(
                os.path.join(
                    gabra_converter.path, '..', '..', 'tests', 'export', 'test_input',
                    'wordforms.jsonl'
                ),
                'r', encoding='utf-8'
            ) as f:
                for line in f:
                    wordform_exporter.add_row(WordformRow(**json.loads(line.strip())), lexeme_ids)

            self.assertEqual(
                set(os.listdir(tmp_path)),
                set(os.listdir(
                    os.path.join(
                        gabra_converter.path, '..', '..', 'tests', 'export', 'test_expected'
                    )
                )) - {'__init__.py', '__pycache__'},
            )
            for fname in os.listdir(tmp_path):
                with open(
                    os.path.join(
                        gabra_converter.path, '..', '..', 'tests', 'export', 'test_expected', fname
                    ),
                    'r', encoding='utf-8'
                ) as f:
                    expected_output = f.readlines()
                with open(os.path.join(tmp_path, fname), 'r', encoding='utf-8') as f:
                    actual_output = f.readlines()
                self.assertEqual(expected_output, actual_output, msg=fname)


#########################################
if __name__ == '__main__':
    unittest.main()
