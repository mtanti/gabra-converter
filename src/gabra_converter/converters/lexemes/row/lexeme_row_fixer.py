'''
Code for fixing lexeme rows in the Ġabra database that do not match the specification.

Specification is from schema in https://mlrs.research.um.edu.mt/resources/gabra-api/p/schema.
'''

from typing import Any


__all__ = [
    'InvalidLexemeException',
    'fix_lexeme_row',
]


#########################################
class InvalidLexemeException(Exception):
    '''Raised when a lexeme row does not conform to the schema.'''


#########################################
def _fix_float_derived_form(
    row: dict[str, Any],
) -> None:
    '''
    Fix rows that have a derived float number as a form field value instead of an integer by
    converting it to an integer value.

    :param row: A row from the lexemes collection.
    '''
    if 'derived_form' in row and '$numberDouble' in row['derived_form']:
        assert len(row['derived_form']) == 1
        assert isinstance(row['derived_form']['$numberDouble'], str)
        assert row['derived_form']['$numberDouble'].endswith('.0')
        row['derived_form'] = {
            '$numberInt': int(float(row['derived_form']['$numberDouble']))
        }


#########################################
def _fix_empty_root(
    row: dict[str, Any],
) -> None:
    '''
    Fix rows that have a root field value set to an empty object by removing the root field.

    :param row: A row from the lexemes collection.
    '''
    if 'root' in row and len(row['root']) == 0:
        del row['root']


#########################################
def _fix_root_without_radicals(
    row: dict[str, Any],
) -> None:
    '''
    Fix rows that have a root field object with a variant key but not a radicals key by removing
    the root field.

    :param row: A row from the lexemes collection.
    '''
    if 'root' in row and len(row['root']) == 1 and 'radicals' not in row['root']:
        assert 'variant' in row['root']
        assert '$numberInt' in row['root']['variant']
        del row['root']


#########################################
def fix_lexeme_row(
    row: dict[str, Any],
) -> dict[str, Any]:
    '''
    Fix rows in the lexemes collection that diverge from the specification.

    :param row: A row from the lexemes collection.
    :return: A reference to ``row``.
    '''
    _fix_float_derived_form(row)
    _fix_empty_root(row)
    _fix_root_without_radicals(row)
    return row
