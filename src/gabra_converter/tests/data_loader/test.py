'''
Test the data_loader requirement.
'''

import os
import unittest
import json
import gabra_converter
from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow
from gabra_converter.converters.lexemes.row.lexeme_row_fixer import fix_lexeme_row
from gabra_converter.converters.wordforms.row.wordform_row import WordformRow
from gabra_converter.converters.wordforms.row.wordform_row_fixer import fix_wordform_row


#########################################
class TestLexemes(unittest.TestCase):
    '''
    Test the lexemes loader.
    '''

    def test_fix(self) -> None:
        '''
        Test that fixable divergences from the lexemes schema are fixed.
        '''
        with open(
            os.path.join(gabra_converter.path, 'tests', 'data_loader', 'test_set_lexemes.json'),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            fix_lexeme_row(entry['input'])
            output = LexemeRow(**entry['input'])
            self.assertEqual(
                output,
                LexemeRow(**entry['expected_output']),
                entry['description'],
            )


#########################################
class TestWordforms(unittest.TestCase):
    '''
    Test the wordforms loader.
    '''

    def test_skip(self) -> None:
        '''
        Test that unfixable divergences from the wordforms schema are skipped.
        '''
        with open(
            os.path.join(
                gabra_converter.path, 'tests', 'data_loader', 'test_set_wordforms_skip.json'
            ),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            with self.assertRaises(Exception, msg=entry['description']):
                fix_wordform_row(entry['input'])

    def test_fix(self) -> None:
        '''
        Test that fixable divergences from the wordforms schema are fixed.
        '''
        with open(
            os.path.join(
                gabra_converter.path, 'tests', 'data_loader', 'test_set_wordforms_fix.json'
            ),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            fix_wordform_row(entry['input'])
            output = WordformRow(**entry['input'])
            self.assertEqual(
                output,
                WordformRow(**entry['expected_output']),
                entry['description'],
            )


#########################################
if __name__ == '__main__':
    unittest.main()
