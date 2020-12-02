from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import re
import pandas as pd
from sys import stderr

import helperFuncs as hf
from db import url_db, Base
from models.Regiao import RegiaoModel
from models.SubRegiao import SubRegiaoModel
from models.SubPrefeitura import SubPrefeituraModel
from models.Distrito import DistritoModel
from models.Bairro import BairroModel
from models.Location import LocationModel
from models.FeiraLivreModel import FeiraLivreModel


def importCsv2SqliteTable(path2csv, path2db=url_db):
    print('Starting Importation',file=stderr)
    dict_result = {'nu_sev': 0, 'log': '', 'is_ok': False}
    path2csv = hf.check_exists_file(path2csv)
    if path2csv['exists'] == False:
        dict_result['nu_sev'] = 3
        dict_result['log'] += '\r\n enter an valid CSV path'

    if dict_result['nu_sev'] == 3:
        return dict_result

    if __validate_csvHeaderXlines(path2csv):
        try:
            df_csv = pd.read_csv(filepath_or_buffer=path2csv['pathFound'], encoding="ISO-8859-1")



            from Importation.config_importation import dict_crossCsvHeader2dbHeaders
            dict_config_importation = dict_crossCsvHeader2dbHeaders

            some_engine = create_engine(path2db)
            Session = sessionmaker(bind=some_engine)
            session = Session()
            Base.metadata.create_all(bind=some_engine)
            for index, row in df_csv.iterrows():
                cell = None
                for config in dict_config_importation:
                    cell = row[config['NameHeaderInCSV']]
                    if config['expected_type'] == type(cell) or None == type(cell):
                        if config['NameHeaderInCSV'] == 'LONG' or config['NameHeaderInCSV'] == 'LAT':
                            len_latLong = len(str(cell))
                            if len_latLong != 9:
                                pass
                            else:
                                cell = re.sub(r'(\-\d{2})(\d+)', r'\1.\2', str(cell))
                        if config['NameHeaderInCSV'] == 'NUMERO':
                           if len(str(cell)) == 0 or re.search(r'^\s+$', cell) is not None:
                                cell = 'N/M'
                        if config['expected_type'] == str:
                            cell = hf.clean_data_str(cell)
                            if re.search(r'\b[A-Z]{2,4}\b', cell, re.IGNORECASE):
                                cell = __sub_shorten_word(cell)

                            cell = cell.capitalize()
                        row[config['NameHeaderInCSV']] = cell
                    else:
                        convert = None
                        try:
                            convert = config['expected_type'](row[config['NameHeaderInCSV']])
                        except Exception as e:
                            print(f'Tried to convert the cell: {cell} to the type {config["expected_type"]},'
                                  f'the following exception was given:\n{repr(e)}\n,please TYPE the correct '
                                  f'data for line {index}, column {config["NameHeaderInCSV"]}',file=stderr )
                            convert = input()
                        row[config['NameHeaderInCSV']] = convert

                __insertRowInSql(row=row, session=session)

            session.close()
            dict_result['is_ok'] = True
            dict_result['log'] = 'The Convertion went sucessfull'
            print('Ending Importation', file=stderr)
            return dict_result

        except Exception as e:
            dict_result['nu_sev'] = 3
            dict_result['log'] = f'The convertion of the csv {path2csv} has go wrong with pd.read_csv, given the Exception:{repr(e)}'
            return dict_result

    else:
        dict_result['nu_sev'] = 3
        dict_result['log'] += '\r\n the csv data does not have the same numbers of positions compared with the headers'
        return dict_result

def __validate_csvHeaderXlines(alignment_filename):
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

def __sub_shorten_word(word, dict_shorten='default'):
    if dict_shorten == 'default':
        from Importation.config_importation import list_shortenWord2completeWord
        dict_shorten = list_shortenWord2completeWord
    for value in dict_shorten:
        pattern_check = rf"(\b{value['shorten']}\b)"
        check = re.search(pattern_check, word, re.IGNORECASE)
        if check:
            word = re.sub(pattern_check, value['complete'], word)

    return word

def __insertRowInSql(row, session):

    New_RegiaoModel = session.query(RegiaoModel).filter(RegiaoModel.name == row['REGIAO5']).first()
    if New_RegiaoModel is None:
        New_RegiaoModel = RegiaoModel(row['REGIAO5'])
        session.add(New_RegiaoModel)
        session.commit()
    # ---------------------------------------------------------------
    New_SubRegiaoModel = session.query(SubRegiaoModel).filter(SubRegiaoModel.name == row['REGIAO8']).first()
    if New_SubRegiaoModel is None:
        New_SubRegiaoModel = SubRegiaoModel(row['REGIAO8'], New_RegiaoModel.id)
        session.add(New_SubRegiaoModel)
        session.commit()
    # ---------------------------------------------------------------
    New_SubPrefeituraModel = session.query(SubPrefeituraModel).filter(SubPrefeituraModel.name == row['SUBPREFE']).first()
    if New_SubPrefeituraModel is None:
        New_SubPrefeituraModel = SubPrefeituraModel(name=row['SUBPREFE'],
                                                    id=row['CODSUBPREF'],
                                                    sub_regiao_id=New_SubRegiaoModel.id)
        session.add(New_SubPrefeituraModel)
        session.commit()
    # ---------------------------------------------------------------
    New_DistritoModel = session.query(DistritoModel).filter(DistritoModel.name == row['DISTRITO']).first()
    if New_DistritoModel is None:
        New_DistritoModel = DistritoModel(name=row['DISTRITO'],
                                          id=row['CODDIST'],
                                          sub_prefeitura_id=New_SubPrefeituraModel.id)
        session.add(New_DistritoModel)
        session.commit()
    # ---------------------------------------------------------------
    New_BairroModel = session.query(BairroModel).filter(BairroModel.name == row['BAIRRO']).first()
    if New_BairroModel is None:
        New_BairroModel = BairroModel(name=row['BAIRRO'],
                                      distrito_id=New_DistritoModel.id)
        session.add(New_BairroModel)
        session.commit()
    # ---------------------------------------------------------------
    New_LocationModel = session.query(LocationModel).filter(LocationModel.long == row['LONG']).\
        filter(LocationModel.lat == row['LAT']).first()
    if New_LocationModel is None:
        New_LocationModel = LocationModel(lat=row['LAT'], long=row['LONG'], endereco=row['LOGRADOURO'],
                                          numero=row['NUMERO'], area_pond=row['AREAP'], setor_cens=row['SETCENS'],
                                          referencia=row['REFERENCIA'], bairro_id=New_BairroModel.id
                                          )
        session.add(New_LocationModel)
        session.commit()
    # ---------------------------------------------------------------
    New_FeiraLivreModel = session.query(FeiraLivreModel).filter(FeiraLivreModel.cod_registro == row['REGISTRO']).first()
    if New_FeiraLivreModel is None:
        New_FeiraLivreModel = FeiraLivreModel(name_feira=row['NOME_FEIRA'],
                                              cod_registro=row['REGISTRO'],
                                              location_id=New_LocationModel.id)
        New_FeiraLivreModel.id = row['ID']
        session.add(New_FeiraLivreModel)
        session.commit()
