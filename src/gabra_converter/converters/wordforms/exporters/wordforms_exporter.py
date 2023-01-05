'''
Export wordform rows to some file format.
'''

from abc import ABC
from gabra_converter.converters.wordforms.row.wordform_row import WordformRow


__all__ = [
    'AddingWordformRowBeforeFilesCreationException',
    'WordformsExporter'
]


#########################################
class AddingWordformRowBeforeFilesCreationException(Exception):
    '''
    A WordformsExporter object was used to add a row to a set of files before creating them.
    '''


#########################################
class WordformsExporter(ABC):
    '''
    Abstract class to be inherited by classes used to export wordform rows into some file format.
    '''

    #########################################
    def __init__(
        self,
    ) -> None:
        '''
        Initialiser.
            Must be called by subclass.
        '''
        self.out_dir_path: str = ''
        self.__files_created: bool = False

    #########################################
    def create(
        self,
        out_dir_path: str,
    ) -> None:
        '''
        Create a new set of files.
            Must be overriden and called by subclass.

        :param out_dir_path: The directory path to a folder to contain the files.
        '''
        self.out_dir_path = out_dir_path
        self.__files_created = True

    #########################################
    def add_row(
        self,
        lexemes_id_map: dict[str, int], # pylint: disable=unused-argument
        row: WordformRow, # pylint: disable=unused-argument
    ) -> None:
        '''
        Add a row to the current set of files.
            Must be overriden and called by subclass.

        :param lexemes_id_map: a dictionary mapping lexeme Ġabra IDs to integer IDs.
            This is returned by a LexemesExporter object.
        :param row: A wordform row to be exported and appended to the files.
        '''
        if not self.__files_created:
            raise AddingWordformRowBeforeFilesCreationException()
