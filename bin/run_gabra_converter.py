#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2024 Marc Tanti
#
# This file is part of Ġabra Converter project.
'''
Convert a Ġabra database dump into a more accessible format.
'''

import os
import argparse
import gabra_converter
from gabra_converter.converters.lexemes.row.lexeme_row import LexemeRow
from gabra_converter.converters.wordforms.row.wordform_row import WordformRow
from gabra_converter.pipeline import pipeline, PipelineListener
from gabra_converter.converters.lexemes.pipeline.listeners.lexeme_pipeline_listener \
    import LexemePipelineListener
from gabra_converter.converters.lexemes.pipeline.listeners.lexeme_pipeline_listener_skip_log \
    import LexemePipelineListenerSkipLog
from gabra_converter.converters.wordforms.pipeline.listeners.wordform_pipeline_listener \
    import WordformPipelineListener
from gabra_converter.converters.wordforms.pipeline.listeners.wordform_pipeline_listener_skip_log \
    import WordformPipelineListenerSkipLog
from gabra_converter.converters.lexemes.exporters.lexeme_exporter_list import (
    get_all_lexeme_exporters
)
from gabra_converter.converters.lexemes.cleaners.lexeme_cleaner_list import (
    get_all_lexeme_cleaners
)
from gabra_converter.converters.wordforms.exporters.wordform_exporter_list import (
    get_all_wordform_exporters
)
from gabra_converter.converters.wordforms.cleaners.wordform_cleaner_list import (
    get_all_wordform_cleaners
)


#########################################
class Listener(PipelineListener):
    '''
    Listens to the different high level stages in the pipeline process.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
        '''
        super().__init__()

    #########################################
    def started_extracting(
        self,
    ) -> None:
        '''
        Listen for when the compressed database dump started being extracted into BSON files.
        '''
        print('Extracting and processing database dump.')

    #########################################
    def started_exporting_lexemes(
        self,
    ) -> None:
        '''
        Listen for when the lexemes JSONL file started being exported into the target format.
        '''
        print('Exporting lexemes...')

    #########################################
    def ended_exporting_lexemes(
        self,
    ) -> None:
        '''
        Listen for when the lexemes JSONL file stopped being exported into the target format.
        '''
        print()

    #########################################
    def started_exporting_wordforms(
        self,
    ) -> None:
        '''
        Listen for when the wordforms JSONL file started being exported into the target format.
        '''
        print('Exporting wordforms...')

    #########################################
    def ended_exporting_wordforms(
        self,
    ) -> None:
        '''
        Listen for when the wordforms JSONL file stopped being exported into the target format.
        '''
        print()


#########################################
class LexemePipelineListener_(LexemePipelineListener):
    '''
    Lexeme pipeline listener.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
        '''
        super().__init__()
        self.count = 0

    #########################################
    def row_exported(
        self,
        json_line: str,
        row: LexemeRow,
    ) -> None:
        '''
        Listen for when a row is successfully exported.

        :param json_line: The raw JSON line that was processed.
        :param row: The processed row that was exported.
        '''
        self.count += 1
        print(f'\r > Rows exported: {self.count}', end='')


#########################################
class WordformPipelineListener_(WordformPipelineListener):
    '''
    Wordform pipeline listener.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
        '''
        super().__init__()
        self.count = 0

    #########################################
    def row_exported(
        self,
        json_line: str,
        row: WordformRow,
    ) -> None:
        '''
        Listen for when a row is successfully exported.

        :param json_line: The raw JSON line that was processed.
        :param row: The processed row that was exported.
        '''
        self.count += 1
        print(f'\r > Rows exported: {self.count}', end='')


#########################################
def main(
) -> None:
    id_to_lexeme_exporter = {exporter.id_: exporter for exporter in get_all_lexeme_exporters()}
    id_to_wordform_exporter = {exporter.id_: exporter for exporter in get_all_wordform_exporters()}
    id_to_lexeme_cleaner = {cleaner.id_: cleaner for cleaner in get_all_lexeme_cleaners()}
    id_to_wordform_cleaner = {cleaner.id_: cleaner for cleaner in get_all_wordform_cleaners()}

    parser = argparse.ArgumentParser(
        description='Convert a Ġabra database dump into a more accessible format.'
    )

    parser.add_argument(
        '-v',
        '--version',
        action='version',
        version='%(prog)s ' + gabra_converter.__version__,
    )

    parser.add_argument(
        '--gabra_dump_path',
        required=True,
        help='The path to the .tar.gz Ġabra dump file downloaded from the website.',
    )
    parser.add_argument(
        '--out_path',
        required=False,
        default='.',
        help=(
            'The path to a folder that will contain the output files.'
            ' The path will be created if it doesn\'t exist.'
        ),
    )
    parser.add_argument(
        '--lexeme_cleaners',
        required=False,
        nargs='*',
        choices=sorted(id_to_lexeme_cleaner.keys()),
        default=[],
        help=(
            'A list of cleaners to apply to the lexemes.'
            ' The following cleaners can be used -'
            ' ' + '; '.join(
                f'*{id_}*: {id_to_lexeme_cleaner[id_].description}'
                for id_ in sorted(id_to_lexeme_cleaner.keys())
            )
        ),
    )
    parser.add_argument(
        '--wordform_cleaners',
        required=False,
        nargs='*',
        choices=sorted(id_to_wordform_cleaner.keys()),
        default=[],
        help=(
            'A list of cleaners to apply to the wordforms.'
            ' The following cleaners can be used -'
            ' ' + '; '.join(
                f'*{id_}*: {id_to_wordform_cleaner[id_].description}'
                for id_ in sorted(id_to_wordform_cleaner.keys())
            )
        ),
    )
    parser.add_argument(
        '--lexeme_exporter',
        required=True,
        choices=sorted(id_to_lexeme_exporter.keys()),
        help=(
            'An exporter to apply to the lexemes.'
            ' The following exporters can be used -'
            ' ' + '; '.join(
                f'*{id_}*: {id_to_lexeme_exporter[id_].description}'
                for id_ in sorted(id_to_lexeme_exporter.keys())
            )
        ),
    )
    parser.add_argument(
        '--wordform_exporter',
        required=True,
        choices=sorted(id_to_wordform_exporter.keys()),
        help=(
            'An exporter to apply to the wordforms.'
            ' The following exporters can be used -'
            ' ' + '; '.join(
                f'*{id_}*: {id_to_wordform_exporter[id_].description}'
                for id_ in sorted(id_to_wordform_exporter.keys())
            )
        ),
    )

    args = parser.parse_args()

    if not args.gabra_dump_path.endswith('.tar.gz'):
        print('Error: gabra_dump_path must point to a .tar.gz file.')
        return

    missing_required_cleaners = (
        id_to_lexeme_exporter[args.lexeme_exporter].required_cleaners
        - set(args.lexeme_cleaners)
    )
    if len(missing_required_cleaners) > 0:
        missing = ', '.join(sorted(missing_required_cleaners))
        print(
            f'The following cleaners are required with lexeme exporter {args.lexeme_exporter}'
            f' but were not used: {missing}'
        )
        return

    missing_required_cleaners = (
        id_to_wordform_exporter[args.wordform_exporter].required_cleaners
        - set(args.wordform_cleaners)
    )
    if len(missing_required_cleaners) > 0:
        missing = ', '.join(sorted(missing_required_cleaners))
        print(
            f'The following cleaners are required with wordforms exporter {args.wordform_exporter}'
            f' but were not used: {missing}'
        )
        return

    print('Starting process.')
    os.makedirs(os.path.abspath(args.out_path))
    lexeme_skip_log = LexemePipelineListenerSkipLog()
    lexeme_skip_log.create(os.path.abspath(args.out_path))
    wordform_skip_log = WordformPipelineListenerSkipLog()
    wordform_skip_log.create(os.path.abspath(args.out_path))
    pipeline(
        gabra_dump_path=os.path.abspath(args.gabra_dump_path),
        out_path=os.path.abspath(args.out_path),
        lexeme_cleaners=[id_to_lexeme_cleaner[id_] for id_ in args.lexeme_cleaners],
        wordform_cleaners=[id_to_wordform_cleaner[id_] for id_ in args.wordform_cleaners],
        lexeme_exporter=id_to_lexeme_exporter[args.lexeme_exporter],
        wordform_exporter=id_to_wordform_exporter[args.wordform_exporter],
        lexeme_pipeline_listeners=[lexeme_skip_log, LexemePipelineListener_()],
        wordform_pipeline_listeners=[wordform_skip_log, WordformPipelineListener_()],
        pipeline_listeners=[Listener()],
    )
    print('Process ready.')


if __name__ == '__main__':
    main()
