#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright © 2022 Marc Tanti
#
# This file is part of Ġabra Converter project.
'''
Validate the project files.
'''

import os
import argparse
import ast
from typing import Any
import gabra_converter


#########################################
def check_init(
    code_path: str,
) -> None:
    '''
    Check for any missing __init__.py files.

    :param code_path: The path to the code files.
    '''
    names = os.listdir(code_path)

    if '__init__.py' not in names:
        raise AssertionError(f'Missing __init__.py in {code_path}.')

    for name in names:
        new_path = os.path.join(code_path, name)
        if os.path.isdir(new_path) and name not in [
            '__pycache__',
        ]:
            check_init(new_path)


#########################################
def check_docs(
    code_path: str,
    doc_path: str,
) -> None:
    '''
    Check for any missing Sphinx documents together.

    :param code_path: The path to the code files.
    :param doc_path: The path to the Sphinx document files.
    '''
    code_names = os.listdir(code_path)
    doc_names = set(os.listdir(doc_path))
    for name in code_names:
        new_code_path = os.path.join(code_path, name)
        new_doc_path = os.path.join(doc_path, name.replace('.py', '.rst'))

        if os.path.isfile(new_code_path) and name.endswith('.py') and name not in [
            '__init__.py'
        ]:
            if not os.path.isfile(new_doc_path):
                raise AssertionError(f'Missing doc for {new_code_path}.')

            with open(new_doc_path, 'r', encoding='utf-8') as f:
                lines = f.read().strip().split('\n')
                namespace = lines[3][16:].split('.')
                expected_namespace = (
                    ['gabra_converter']
                    + new_code_path.replace('.py', '').split(os.path.sep)[-len(namespace)+1:]
                )
                if namespace != expected_namespace:
                    raise AssertionError(f'Wrong namespace for {new_doc_path}.')

        if os.path.isdir(new_code_path) and name not in [
            '__pycache__',
            'tests',
        ]:
            if name not in doc_names:
                raise AssertionError(f'Missing doc directory for {new_code_path}.')
            if f'{name}.rst' not in doc_names:
                raise AssertionError(f'Missing doc for {new_code_path}.')

            check_docs(new_code_path, new_doc_path)


#########################################
def check_docstrings_file(
    path: str,
    tree: Any,
) -> None:
    '''
    Check the docstrings in a single file.

    :param path: The path to the file being checked (used for error messages).
    :param tree: The abstract syntax tree of the code (produced by ast.parse).
    '''
    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            if (
                not isinstance(node.body[0], ast.Expr)
                or not isinstance(node.body[0].value, ast.Str)
            ):
                raise AssertionError(
                    f'Missing docstring in class {node.name} on line {node.lineno}'
                    f' in file {path}.'
                )
            check_docstrings_file(path, node)

        if isinstance(node, ast.FunctionDef):
            name: str = node.name
            line_num: int = node.lineno
            args: list[str] = [arg.arg for arg in node.args.args if arg.arg != 'self']
            assert node.returns is not None
            has_return = (
                not isinstance(node.returns, ast.NameConstant)
                or node.returns.value is not None
            )
            if (
                not isinstance(node.body[0], ast.Expr)
                or not isinstance(node.body[0].value, ast.Str)
            ):
                raise AssertionError(
                    f'Missing docstring in function {name} on line {line_num}'
                    f' in file {path}.'
                )
            docstring: str = node.body[0].value.s

            args_mentioned = []
            return_mentioned = False
            for line in docstring.split('\n'):
                line = line.strip()
                if line.startswith(':param '):
                    arg = line.split(' ')[1][:-1]
                    args_mentioned.append(arg)
                if line.startswith(':return:'):
                    return_mentioned = True
            if args != args_mentioned:
                raise AssertionError(
                    f'The docstring in function {name} on line {line_num}'
                    f' in file {path} does not match the function\'s arguments.'
                    ' Arguments in docstring but not in function: {}.'
                    ' Arguments in function but not in docstring: {}.'
                    .format(
                        sorted(set(args_mentioned) - set(args)),
                        sorted(set(args) - set(args_mentioned)),
                    )
                )
            if has_return != return_mentioned:
                raise AssertionError(
                    f'The docstring in function {name} on line {line_num}'
                    f' in file {path} does not match the function\'s return annotation.'
                )


#########################################
def check_docstrings(
    code_path: str,
) -> None:
    '''
    Check for any missing Sphinx documents together.

    :param code_path: The path to the code files.
    '''
    names = os.listdir(code_path)

    for name in names:
        new_path = os.path.join(code_path, name)

        if os.path.isfile(new_path) and name.endswith('.py') and name not in [
            '__init__.py'
        ]:
            with open(new_path, 'r', encoding='utf-8') as f:
                tree: Any = ast.parse(f.read())

            if (
                not isinstance(tree.body[0], ast.Expr)
                or not isinstance(tree.body[0].value, ast.Str)
            ):
                raise AssertionError(
                    f'Missing module docstring in file {new_path}.'
                )

            check_docstrings_file(new_path, tree)

        if os.path.isdir(new_path) and name not in [
            '__pycache__',
        ]:
            check_docstrings(new_path)


#########################################
def main(
) -> None:
    '''
    Main function.
    '''
    parser = argparse.ArgumentParser(
        description='Validate the project files.'
    )

    parser.parse_args()

    check_init(gabra_converter.path)

    check_docs(
        gabra_converter.path,
        os.path.abspath(os.path.join(
            gabra_converter.path, '..', 'docs', 'source', 'gabra_converter'
        ))
    )

    check_docstrings(gabra_converter.path)
    check_docstrings(os.path.abspath(os.path.join(gabra_converter.path, '..', 'tools')))


#########################################
if __name__ == '__main__':
    main()
