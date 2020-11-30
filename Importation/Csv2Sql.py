
import pandas as pd
import re


import helperFuncs as hf
from db import url_db


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
    path2csv = hf.check_exists_file(path2csv)
    if path2csv['exists'] == False:
        dict_result['nu_sev'] = 3
        dict_result['log'] += '\r\n enter an valid CSV path'

    if dict_result['nu_sev'] == 3:
        return dict_result

    if validate_csvHeaderXlines(path2csv):
        try:
            df_csv = pd.read_csv(filepath_or_buffer=path2csv['pathFound'], encoding="ISO-8859-1")


            import Importation.config_importation as ci

            dict_config_importation = ci.dict_crossCsvHeader2dbHeaders

            for index, row in df_csv.iterrows():
                for value in dict_config_importation:
                    cell = row[value['NameHeaderInCSV']]
                    if value['expected_type'] == type(cell) or None == type(cell):
                        if value['NameHeaderInCSV'] == 'LONG' or value['NameHeaderInCSV'] == 'LAT':
                            len_latLong = len(str(cell))
                            if len_latLong != 9:
                                cell = ''
                            else:
                                cell = re.sub(r'(\-\d{2})(\d+)', r'\1.\2', str(cell), re.IGNORECASE)
                        if value['NameHeaderInCSV'] == 'NUMERO':
                           if len(str(cell)) == 0 or re.search(r'^\s+$', cell) is not None:
                                cell = 'S/N'

                        ci.RegiaoModel()






                    break
                break

        except Exception as e:
            dict_result['nu_sev'] = 3
            dict_result['log'] = f'The convertion of the csv {path2csv} has go wrong with pd.read_csv, given the Exception:{repr(e)}'
            return dict_result

    else:
        dict_result['nu_sev'] = 3
        dict_result['log'] += '\r\n the csv data does not have the same numbers of positions compared with the headers'
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



path2csv = 'DEINFO_AB_FEIRASLIVRES_2014.csv'
print(importCsv2SqliteTable(path2csv=path2csv, path2db=url_db, name_table='ASD'))