import pandas as pd


from pathlib import Path
import os

def isSQLite3(filename):
    from os.path import isfile, getsize

    if not isfile(filename):
        return False
    if getsize(filename) < 100: # SQLite database file header is 100 bytes
        return False

    with open(filename, 'rb') as fd:
        header = fd.read(100)

    return r'SQLite format 3\x00' in str(header[:16])



def importCsv2SqliteTable(path2db, name_table, path2csv):
    dict_result = {'nu_sev': 0, 'log': '', 'is_ok': False}

    if check_exists_file(path2csv):
        dict_result['nu_sev'] = 3
        dict_result['log'] += '\r\n enter an valid CSV path'

    if dict_result['nu_sev'] == 3:
        return dict_result

    if validate_csvHeaderXlines(path2csv):
        try:
            pd.read_csv(filepath_or_buffer=path2csv)
        except Exception as e:
            dict_result['nu_sev'] = 3
            dict_result['log'] = f'The convertion of the csv {path2csv} has go wrong with pd.read_csv, given the Exception:{repr(e)}'
            return dict_result

    else:
        dict_result['nu_sev'] = 3
        dict_result['log'] += '\r\n the csv data does not have the same numbers of headers'
        return dict_result

def validate_csvHeaderXlines(alignment_filename):
    #todo make this func work correctly, it will basically check if each data line do not trepass the header, and if is false, give the current line with error
    return True
    import csv
    file = open(alignment_filename)
    contentss = csv.reader(file)
    for x in contentss:
        if len(x) == 0:
            return False
        elif int(x[0]) > int(x[1]):
            return False
    return True

def check_exists_file(_file, path2check=''):
    """if path2chek is empty, it will search for the file in root project foulder
         """
    str_path = _file
    if len(path2check) < 1:
        path_w10 = Path(str_path)
        exists = os.path.exists(path_w10)
        return exists
    str_path = fr'{Path().absolute()}\{str_path}'
    print(str_path)
    path_w10 = Path(str_path)
    exists = os.path.exists(path_w10)

    return exists

