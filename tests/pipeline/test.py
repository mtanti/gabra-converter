'''
Test the pipeline requirement.
'''

import os
import tempfile
import unittest
import gabra_converter
from gabra_converter.converters.lexemes.cleaners.lexeme_cleaner_list import (
    get_all_lexeme_cleaners
)
from gabra_converter.converters.lexemes.exporters.lexeme_exporter_list import (
    get_all_lexeme_exporters
)
from gabra_converter.converters.lexemes.pipeline.lexeme_pipeline import LexemePipeline
from gabra_converter.converters.lexemes.pipeline.listeners.lexeme_pipeline_listener_skip_log \
    import LexemePipelineListenerSkipLog
from gabra_converter.converters.wordforms.exporters.wordform_exporter_list import (
    get_all_wordform_exporters
)
from gabra_converter.converters.wordforms.cleaners.wordform_cleaner_list import (
    get_all_wordform_cleaners
)
from gabra_converter.converters.wordforms.pipeline.wordform_pipeline import WordformPipeline
from gabra_converter.converters.wordforms.pipeline.listeners.wordform_pipeline_listener_skip_log \
    import WordformPipelineListenerSkipLog


#########################################
class Test(unittest.TestCase):
    '''
    As described.
    '''

    #########################################
    def test_(
        self,
    ) -> None:
        '''
        Test the pipelines.
        '''
        with tempfile.TemporaryDirectory() as tmp_path:
            lexeme_exporter = [
                exporter for exporter in get_all_lexeme_exporters() if exporter.id_ == 'csv'
            ][0]
            lexeme_cleaners = get_all_lexeme_cleaners()
            lexeme_pipeline = LexemePipeline(lexeme_cleaners, lexeme_exporter)

            lexeme_pipeline_listener = LexemePipelineListenerSkipLog()
            lexeme_pipeline.add_listener(lexeme_pipeline_listener)

            lexeme_pipeline.create(tmp_path)
            lexeme_pipeline_listener.create(tmp_path)

            lexeme_pipeline.convert_file(
                os.path.join(
                    gabra_converter.path, '..', '..', 'tests', 'pipeline', 'test_input',
                    'lexemes.jsonl'
                )
            )
            lexeme_ids = lexeme_pipeline.get_id_map()

            wordform_exporter = [
                exporter for exporter in get_all_wordform_exporters() if exporter.id_ == 'csv'
            ][0]
            wordform_cleaners = get_all_wordform_cleaners()
            wordform_pipeline = WordformPipeline(wordform_cleaners, wordform_exporter)

            wordform_pipeline_listener = WordformPipelineListenerSkipLog()
            wordform_pipeline.add_listener(wordform_pipeline_listener)

            wordform_pipeline.create(tmp_path)
            wordform_pipeline_listener.create(tmp_path)

            wordform_pipeline.convert_file(
                os.path.join(
                    gabra_converter.path, '..', '..', 'tests', 'pipeline', 'test_input',
                    'wordforms.jsonl'
                ),
                lexeme_ids,
            )

            self.assertEqual(
                set(os.listdir(tmp_path)),
                set(os.listdir(
                    os.path.join(
                        gabra_converter.path, '..', '..', 'tests', 'pipeline', 'test_expected'
                    )
                )) - {'__init__.py', '__pycache__'},
            )
            for fname in os.listdir(tmp_path):
                with open(
                    os.path.join(
                        gabra_converter.path, '..', '..', 'tests', 'pipeline',
                        'test_expected', fname
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
