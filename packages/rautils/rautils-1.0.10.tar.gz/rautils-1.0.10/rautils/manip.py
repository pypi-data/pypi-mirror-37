import pandas as pd
import os
from typing import TypeVar


def missingDataFiles(file_names: dict):
    '''
    file_names: dict - dictionary of file names to check if it exists
    '''
    missing_files = [key for key, file_name in file_names.items()
                     if not os.path.isfile(str(file_name))]
    return missing_files


def removeMissingDataFiles(file_names: list or dict):
    '''
    file_names: list/dict - list/dict of file names to check if it exists
    '''
    # file_names = TypeVar(file_names, list, dict)

    if list is type(file_names):
        file_names = [file_name for file_name in file_names
                      if os.path.isfile(str(file_name))]

    elif dict is type(file_names):
        file_names = {key: file_name for (key, file_name) in file_names.items()
                      if os.path.isfile(str(file_name))}

    else:
        raise ValueError('file_names must be type dict|list')

    return file_names
