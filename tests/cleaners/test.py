'''
Test the cleaners requirement.
'''

import os
import unittest
import json
import gabra_converter
from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow
from gabra_converter.converters.lexemes.cleaners.lexeme_cleaner_list import (
    get_all_lexeme_cleaners
)
from gabra_converter.converters.wordforms.row.wordform_row import WordformRow
from gabra_converter.converters.wordforms.cleaners.wordform_cleaner_list import (
    get_all_wordform_cleaners
)


#########################################
class TestLexemes(unittest.TestCase):
    '''
    Test the lexeme cleaners.
    '''

    #########################################
    def test_unique_ids(
        self,
    ) -> None:
        '''
        Test that the IDs in the lexeme cleaners list and in the wordform cleaners list are unique.
        '''
        self.assertCountEqual(
            list({cleaner.id_ for cleaner in get_all_lexeme_cleaners()}),
            [cleaner.id_ for cleaner in get_all_lexeme_cleaners()],
            msg='lexeme cleaners',
        )
        self.assertCountEqual(
            list({cleaner.id_ for cleaner in get_all_wordform_cleaners()}),
            [cleaner.id_ for cleaner in get_all_wordform_cleaners()],
            msg='wordform cleaners',
        )

    #########################################
    def test_new_lines(
        self,
    ) -> None:
        '''
        Test the new lines lexeme cleaner.
        '''
        cleaners = [
            cleaner for cleaner in get_all_lexeme_cleaners()
            if cleaner.id_ == 'new_lines'
        ]
        self.assertEqual(len(cleaners), 1)
        cleaner = cleaners[0]

        with open(
            os.path.join(
                gabra_converter.path, '..', '..', 'tests', 'cleaners',
                'test_set_lexemes_new_lines.json'
            ),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            row = LexemeRow(**entry['input'])
            accepted = cleaner.clean(row)
            self.assertEqual(accepted, entry['accepted'])
            self.assertEqual(
                row,
                LexemeRow(**entry['expected_output']),
                entry['description'],
            )

    #########################################
    def test_lemma_spaces(
        self,
    ) -> None:
        '''
        Test the lemma spaces lexeme cleaner.
        '''
        cleaners = [
            cleaner for cleaner in get_all_lexeme_cleaners()
            if cleaner.id_ == 'lemma_spaces'
        ]
        self.assertEqual(len(cleaners), 1)
        cleaner = cleaners[0]

        with open(
            os.path.join(
                gabra_converter.path, '..', '..', 'tests', 'cleaners',
                'test_set_lexemes_lemma_spaces.json'
            ),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            row = LexemeRow(**entry['input'])
            accepted = cleaner.clean(row)
            self.assertEqual(accepted, entry['accepted'])

    #########################################
    def test_lemma_capitals(
        self,
    ) -> None:
        '''
        Test the lemma capitals lexeme cleaner.
        '''
        cleaners = [
            cleaner for cleaner in get_all_lexeme_cleaners()
            if cleaner.id_ == 'lemma_capitals'
        ]
        self.assertEqual(len(cleaners), 1)
        cleaner = cleaners[0]

        with open(
            os.path.join(
                gabra_converter.path, '..', '..', 'tests', 'cleaners',
                'test_set_lexemes_lemma_capitals.json'
            ),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            row = LexemeRow(**entry['input'])
            accepted = cleaner.clean(row)
            self.assertEqual(accepted, entry['accepted'])

    #########################################
    def test_lemma_nonmaltese(
        self,
    ) -> None:
        '''
        Test the lemma non-Maltese lexeme cleaner.
        '''
        cleaners = [
            cleaner for cleaner in get_all_lexeme_cleaners()
            if cleaner.id_ == 'lemma_nonmaltese'
        ]
        self.assertEqual(len(cleaners), 1)
        cleaner = cleaners[0]

        with open(
            os.path.join(
                gabra_converter.path, '..', '..', 'tests', 'cleaners',
                'test_set_lexemes_lemma_nonmaltese.json'
            ),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            row = LexemeRow(**entry['input'])
            accepted = cleaner.clean(row)
            self.assertEqual(accepted, entry['accepted'])

    #########################################
    def test_pending(
        self,
    ) -> None:
        '''
        Test the pending lexeme cleaner.
        '''
        cleaners = [
            cleaner for cleaner in get_all_lexeme_cleaners()
            if cleaner.id_ == 'pending'
        ]
        self.assertEqual(len(cleaners), 1)
        cleaner = cleaners[0]

        with open(
            os.path.join(
                gabra_converter.path, '..', '..', 'tests', 'cleaners',
                'test_set_lexemes_pending.json'
            ),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            row = LexemeRow(**entry['input'])
            accepted = cleaner.clean(row)
            self.assertEqual(accepted, entry['accepted'])


#########################################
class TestWordforms(unittest.TestCase):
    '''
    Test the wordform cleaners.
    '''

    #########################################
    def test_missing_lexeme(
        self,
    ) -> None:
        '''
        Test the missing lexeme wordform cleaner.
        '''
        cleaners = [
            cleaner for cleaner in get_all_wordform_cleaners()
            if cleaner.id_ == 'missing_lexeme'
        ]
        self.assertEqual(len(cleaners), 1)
        cleaner = cleaners[0]

        with open(
            os.path.join(
                gabra_converter.path, '..', '..', 'tests', 'cleaners',
                'test_set_wordforms_missing_lexeme.json'
            ),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            row = WordformRow(**entry['input'])
            accepted = cleaner.clean(row, entry['lexemes_id_map'])
            self.assertEqual(accepted, entry['accepted'])
            self.assertEqual(
                row,
                WordformRow(**entry['expected_output']),
                entry['description'],
            )

    #########################################
    def test_surfaceform_capitals(
        self,
    ) -> None:
        '''
        Test the surfaceform capitals wordform cleaner.
        '''
        cleaners = [
            cleaner for cleaner in get_all_wordform_cleaners()
            if cleaner.id_ == 'surfaceform_capitals'
        ]
        self.assertEqual(len(cleaners), 1)
        cleaner = cleaners[0]

        with open(
            os.path.join(
                gabra_converter.path, '..', '..', 'tests', 'cleaners',
                'test_set_wordforms_surfaceform_capitals.json'
            ),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            row = WordformRow(**entry['input'])
            accepted = cleaner.clean(row, entry['lexemes_id_map'])
            self.assertEqual(accepted, entry['accepted'])

    #########################################
    def test_surfaceform_spaces(
        self,
    ) -> None:
        '''
        Test the surfaceform spaces wordform cleaner.
        '''
        cleaners = [
            cleaner for cleaner in get_all_wordform_cleaners()
            if cleaner.id_ == 'surfaceform_spaces'
        ]
        self.assertEqual(len(cleaners), 1)
        cleaner = cleaners[0]

        with open(
            os.path.join(
                gabra_converter.path, '..', '..', 'tests', 'cleaners',
                'test_set_wordforms_surfaceform_spaces.json'
            ),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            row = WordformRow(**entry['input'])
            accepted = cleaner.clean(row, entry['lexemes_id_map'])
            self.assertEqual(accepted, entry['accepted'])

    #########################################
    def test_surfaceform_nonmaltese(
        self,
    ) -> None:
        '''
        Test the surfaceform non-Maltese wordform cleaner.
        '''
        cleaners = [
            cleaner for cleaner in get_all_wordform_cleaners()
            if cleaner.id_ == 'surfaceform_nonmaltese'
        ]
        self.assertEqual(len(cleaners), 1)
        cleaner = cleaners[0]

        with open(
            os.path.join(
                gabra_converter.path, '..', '..', 'tests', 'cleaners',
                'test_set_wordforms_surfaceform_nonmaltese.json'
            ),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            row = WordformRow(**entry['input'])
            accepted = cleaner.clean(row, entry['lexemes_id_map'])
            self.assertEqual(accepted, entry['accepted'])

    #########################################
    def test_pending(
        self,
    ) -> None:
        '''
        Test the pending wordform cleaner.
        '''
        cleaners = [
            cleaner for cleaner in get_all_wordform_cleaners()
            if cleaner.id_ == 'pending'
        ]
        self.assertEqual(len(cleaners), 1)
        cleaner = cleaners[0]

        with open(
            os.path.join(
                gabra_converter.path, '..', '..', 'tests', 'cleaners',
                'test_set_wordforms_pending.json'
            ),
            'r', encoding='utf-8'
        ) as f:
            test_set = json.load(f)

        for entry in test_set:
            row = WordformRow(**entry['input'])
            accepted = cleaner.clean(row, entry['lexemes_id_map'])
            self.assertEqual(accepted, entry['accepted'])


#########################################
if __name__ == '__main__':
    unittest.main()
