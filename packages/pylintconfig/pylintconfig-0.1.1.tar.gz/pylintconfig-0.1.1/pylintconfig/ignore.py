# This command is not yet finished and should not be connected to the cli.
# In order for this to work properly, the existing pylintrc file needs to be found and parsed.

import os
import subprocess

import click


def _get_files_per_error(code_path: str) -> dict:

    if not os.path.exists(code_path):
        raise IOError('Invalid code_path')

    result = subprocess.check_output(['pylint', "--msg-template='# {path} {symbol}'", code_path, '--exit-zero'])

    symbols = {}
    for line in result.decode('utf-8').splitlines():

        if line.startswith('#'):
            _, file_path, symbol = line.split(' ')
            file_name = file_path.split('/')[-1]

            if symbol in symbols:
                symbols[symbol].append(file_name)
            else:
                symbols[symbol] = [file_name]

    return symbols


def _print_pylintrc_content(errors: dict):
    if errors:

        print('[MASTER]')
        for i, (error, file_names) in enumerate(errors.items()):
            for j, file_name in enumerate(file_names):
                if i == 0 and j == 0:
                    print("ignore={0:30} # {1}".format(f'{file_name},', error))
                elif i != 0 and j == 0:
                    print("")
                    print("       {0:30} # {1}".format(f'{file_name},', error))
                else:
                    print("       {0:30}".format(f'{file_name},'))


@click.command()
@click.argument('modules_or_packages')
def ignore(modules_or_packages):
    """
    Run pylint and output the contents of a pylintrc file with all error files explicitly ignored.
    This command is very useful when you want to enable specific errors. Explicitly ignoring these files
    enables checking these errors on new files, and creating a todo list for necessary changes in the codebase.
    """
    errors = _get_files_per_error(modules_or_packages)
    _print_pylintrc_content(errors)
