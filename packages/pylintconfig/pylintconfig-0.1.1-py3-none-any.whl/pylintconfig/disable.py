import os
import subprocess

import click


def _get_current_errors(code_path: str) -> set:
    symbols = set()

    if not os.path.exists(code_path):
        raise IOError('Invalid path')

    result = subprocess.check_output(['pylint', "--msg-template='# {msg_id}: {symbol}'", code_path, '--exit-zero'])

    for line in result.decode('utf-8').splitlines():
        if line.startswith('#'):
            _, symbol = line.split(':')
            symbols.add(symbol.strip())

    return symbols


def _print_pylintrc_content(symbols: set):
    print('[MESSAGES CONTROL]')
    for i, symbol in enumerate(symbols):
        if i == 0:
            print(f'disable={symbol},')
        else:
            print(f'        {symbol},')


@click.command()
@click.argument('modules_or_packages')
def disable(modules_or_packages):
    """
    Run pylint and output the contents of a pylintrc file with all errors explicitly disabled.
    This command is very useful for an initial setup of pylint in an existing codebase.

    Don't execute this command when you already have a pylintrc file, 
    which disables errors. These suppressed errors will not be present in the output config file and
    will lead to confusing results.

    """
    error_symbols = _get_current_errors(modules_or_packages)
    _print_pylintrc_content(error_symbols)
