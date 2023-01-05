'''
Test the export requirement.
'''

import os
import tempfile
import unittest
import json
import gabra_converter
from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow
from gabra_converter.converters.lexemes.exporters.csv_lexemes_exporter import CSVLexemesExporter
from gabra_converter.converters.wordforms.row.wordform_row import WordformRow
from gabra_converter.converters.wordforms.exporters.csv_wordforms_exporter import (
    CSVWordformsExporter
)


#########################################
class Test(unittest.TestCase):
    '''
    As described.
    '''

    def test_csv(self) -> None:
        '''
        Test the CSV exporters.
        '''
        with tempfile.TemporaryDirectory() as tmp_path:
            lexemes_exporter = CSVLexemesExporter()
            lexemes_exporter.create(tmp_path)
            with open(
                os.path.join(
                    gabra_converter.path, 'tests', 'export', 'test_input', 'lexemes.jsonl'
                ),
                'r', encoding='utf-8'
            ) as f:
                for line in f:
                    lexemes_exporter.add_row(LexemeRow(**json.loads(line.strip())))
            lexeme_ids = lexemes_exporter.get_id_map()

            wordforms_exporter = CSVWordformsExporter()
            wordforms_exporter.create(tmp_path)
            with open(
                os.path.join(
                    gabra_converter.path, 'tests', 'export', 'test_input', 'wordforms.jsonl'
                ),
                'r', encoding='utf-8'
            ) as f:
                for line in f:
                    wordforms_exporter.add_row(lexeme_ids, WordformRow(**json.loads(line.strip())))

            self.assertEqual(
                set(os.listdir(tmp_path)),
                set(os.listdir(
                    os.path.join(gabra_converter.path, 'tests', 'export', 'test_expected')
                )) - {'__init__.py', '__pycache__'},
            )
            for fname in os.listdir(tmp_path):
                with open(
                    os.path.join(gabra_converter.path, 'tests', 'export', 'test_expected', fname),
                    'r', encoding='utf-8'
                ) as f:
                    expected_output = f.readlines()
                with open(os.path.join(tmp_path, fname), 'r', encoding='utf-8') as f:
                    actual_output = f.readlines()
                self.assertEqual(expected_output, actual_output, msg=fname)


#########################################
if __name__ == '__main__':
    unittest.main()
