'''
Test the archive_extractor requirement.
'''

import os
import tempfile
import unittest
import gabra_converter
from gabra_converter.converters.archive_extractor import (
    extract_archived_files,
    convert_bson_file,
)


#########################################
class Test(unittest.TestCase):
    '''
    As described.
    '''

    #########################################
    def test_archive_extraction(
        self,
    ) -> None:
        '''
        Extract the mock archive and check that it was extracted correctly.
        '''
        with tempfile.TemporaryDirectory() as tmp_path:
            extract_archived_files(
                os.path.join(
                    gabra_converter.path, '..', '..', 'tests', 'archive_extractor',
                    'mock_dump.tar.gz'
                ),
                tmp_path,
            )

            self.assertEqual(
                set(os.listdir(os.path.join(tmp_path))),
                {'tmp'},
            )
            self.assertEqual(
                set(os.listdir(os.path.join(tmp_path, 'tmp'))),
                {'gabra'},
            )
            self.assertEqual(
                set(os.listdir(os.path.join(tmp_path, 'tmp', 'gabra'))),
                {
                    'lexemes.bson',
                    'lexemes.metadata.json',
                    'wordforms.bson',
                    'wordforms.metadata.json',
                },
            )

    #########################################
    def test_bson_conversion(
        self,
    ) -> None:
        '''
        Extract the mock archive and then convert the BSON files to JSON lines files.
        Check that the JSON lines files were extracted and converted correctly.
        '''
        with tempfile.TemporaryDirectory() as tmp_path:
            extract_archived_files(
                os.path.join(
                    gabra_converter.path, '..', '..', 'tests', 'archive_extractor',
                    'mock_dump.tar.gz'
                ),
                tmp_path,
            )

            with open(
                os.path.join(
                    gabra_converter.path, '..', '..', 'tests', 'archive_extractor',
                    'mock_lexemes.jsonl'
                ),
                'r', encoding='utf-8',
            ) as f:
                text_expected = f.read()
            convert_bson_file(
                os.path.join(tmp_path, 'tmp', 'gabra', 'lexemes.bson'),
                os.path.join(tmp_path, 'lexemes.jsonl'),
            )
            with open(os.path.join(tmp_path, 'lexemes.jsonl'), 'r', encoding='utf-8') as f:
                text_actual = f.read()
            self.assertEqual(text_expected, text_actual)

            with open(
                os.path.join(
                    gabra_converter.path, '..', '..', 'tests', 'archive_extractor',
                    'mock_wordforms.jsonl'
                ),
                'r', encoding='utf-8',
            ) as f:
                text_expected = f.read()
            convert_bson_file(
                os.path.join(tmp_path, 'tmp', 'gabra', 'wordforms.bson'),
                os.path.join(tmp_path, 'wordforms.jsonl'),
            )
            with open(os.path.join(tmp_path, 'wordforms.jsonl'), 'r', encoding='utf-8') as f:
                text_actual = f.read()
            self.assertEqual(text_expected, text_actual)


#########################################
if __name__ == '__main__':
    unittest.main()
