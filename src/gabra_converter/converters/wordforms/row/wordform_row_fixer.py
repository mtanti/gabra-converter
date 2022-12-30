'''
Code for fixing wordform rows in the Ġabra database that do not match the specification.

Specification is from schema in https://mlrs.research.um.edu.mt/resources/gabra-api/p/schema.
'''

from typing import Any


__all__ = [
    'InvalidWordformException',
    'MissingRequiredFieldsException',
    'MissingRequiredGrammemeException',
    'fix_wordform_row',
]


#########################################
class InvalidWordformException(Exception):
    '''Raised when a wordform row does not conform to the schema.'''


#########################################
class MissingRequiredFieldsException(InvalidWordformException):
    '''Raised when a wordform row does not have a required field.'''


#########################################
class MissingRequiredGrammemeException(InvalidWordformException):
    '''Raised when a set of grammeme values in a wordform row does not have a required value.'''


#########################################
def _fix_missing_required(
    row: dict[str, Any],
) -> None:
    '''
    Raise an error if the row has its required fields missing.

    :param row: A row from the wordforms collection.
    '''
    if 'lexeme_id' not in row or 'surface_form' not in row:
        raise MissingRequiredFieldsException()


#########################################
def _fix_subject_without_person(
    row: dict[str, Any],
) -> None:
    '''
    Raise an error if a row has a subject with a grammatical person set to none.

    :param row: A row from the wordforms collection.
    '''
    if 'subject' in row and row['subject']['person'] is None:
        raise MissingRequiredGrammemeException()


#########################################
def _fix_alternatives_not_list(
    row: dict[str, Any],
) -> None:
    '''
    Fix alternatives field that is a single instead of a list by putting the string in a list.

    :param row: A row from the wordforms collection.
    '''
    if 'alternatives' in row and isinstance(row['alternatives'], str):
        row['alternatives'] = [row['alternatives']]


#########################################
def _fix_empty_number(
    row: dict[str, Any],
) -> None:
    '''
    Fix number field that is an empty string by removing the number field.

    :param row: A row from the wordforms collection.
    '''
    if 'number' in row and row['number'] == '':
        del row['number']


#########################################
def fix_wordform_row(
    row: dict[str, Any],
) -> dict[str, Any]:
    '''
    Fix rows in the wordform collection that diverge from the specification.

    :param row: A row from the wordforms collection.
    :return: A reference to ``row``.
    '''
    _fix_missing_required(row)
    _fix_subject_without_person(row)
    _fix_alternatives_not_list(row)
    _fix_empty_number(row)
    return row
