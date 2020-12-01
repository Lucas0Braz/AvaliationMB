
from models.FeiraLivreModel import FeiraLivreModel
from models.Location import LocationModel
from models.Bairro import BairroModel
from models.Distrito import DistritoModel
from models.SubPrefeitura import SubPrefeituraModel
from models.SubRegiao import SubRegiaoModel
from models.Regiao import RegiaoModel


#todo get expected_type from obj_sqlAlchemy: sqlalchemy_utils.get_type(FeiraLivreModel.id)
#The order here is important,because will insert each one according to the given position
dict_crossCsvHeader2dbHeaders = [
    {'NameHeaderInCSV': 'REGIAO5', 'expected_type': str, 'prop_sqlAlchemy': RegiaoModel.name, 'sqlAlchemyModel': RegiaoModel},
    {'NameHeaderInCSV': 'REGIAO8', 'expected_type': str, 'prop_sqlAlchemy': SubRegiaoModel.name, 'sqlAlchemyModel': SubRegiaoModel },
    {'NameHeaderInCSV': 'CODSUBPREF', 'expected_type': int, 'prop_sqlAlchemy': SubPrefeituraModel.id, 'sqlAlchemyModel': SubPrefeituraModel },
    {'NameHeaderInCSV': 'SUBPREFE', 'expected_type': str, 'prop_sqlAlchemy': SubPrefeituraModel.name, 'sqlAlchemyModel': SubPrefeituraModel},
    {'NameHeaderInCSV': 'CODDIST', 'expected_type': int, 'prop_sqlAlchemy': DistritoModel.id, 'sqlAlchemyModel': DistritoModel},
    {'NameHeaderInCSV': 'DISTRITO', 'expected_type': str, 'prop_sqlAlchemy': DistritoModel.name, 'sqlAlchemyModel': DistritoModel},
    {'NameHeaderInCSV': 'BAIRRO', 'expected_type': str, 'prop_sqlAlchemy': BairroModel.name, 'sqlAlchemyModel': BairroModel},
    {'NameHeaderInCSV': 'LONG', 'expected_type': float, 'prop_sqlAlchemy': LocationModel.long, 'sqlAlchemyModel': LocationModel },
    {'NameHeaderInCSV': 'LAT', 'expected_type': float, 'prop_sqlAlchemy': LocationModel.lat, 'sqlAlchemyModel': LocationModel },
    {'NameHeaderInCSV': 'SETCENS', 'expected_type': int, 'prop_sqlAlchemy': LocationModel.setor_cens, 'sqlAlchemyModel': LocationModel},
    {'NameHeaderInCSV': 'AREAP', 'expected_type': int, 'prop_sqlAlchemy': LocationModel.area_pond, 'sqlAlchemyModel': LocationModel},
    {'NameHeaderInCSV': 'LOGRADOURO', 'expected_type': str, 'prop_sqlAlchemy': LocationModel.endereco, 'sqlAlchemyModel': LocationModel},
    {'NameHeaderInCSV': 'NUMERO', 'expected_type': str, 'prop_sqlAlchemy': LocationModel.numero, 'sqlAlchemyModel': LocationModel},
    {'NameHeaderInCSV': 'REFERENCIA', 'expected_type': str, 'prop_sqlAlchemy': LocationModel.referencia, 'sqlAlchemyModel': LocationModel},
    {'NameHeaderInCSV': 'ID', 'expected_type': int, 'prop_sqlAlchemy': FeiraLivreModel.id, 'sqlAlchemyModel': FeiraLivreModel},
    {'NameHeaderInCSV': 'NOME_FEIRA', 'expected_type': str, 'prop_sqlAlchemy': FeiraLivreModel.name_feira, 'sqlAlchemyModel': FeiraLivreModel},
    {'NameHeaderInCSV': 'REGISTRO', 'expected_type': str, 'prop_sqlAlchemy': FeiraLivreModel.cod_registro, 'sqlAlchemyModel': FeiraLivreModel},
]

list_shortenWord2completeWord = [
    {'shorten': 'VL', 'complete': 'Vila'},
    {'shorten': 'PQ', 'complete': 'Parque'},
    {'shorten': 'STA', 'complete': 'Santa'},
    {'shorten': 'JD', 'complete': 'Jardim'},
    {'shorten': 'CID', 'complete': 'Cidade'},
    {'shorten': 'ENG', 'complete': 'Engenheiro'},
]


for config in dict_crossCsvHeader2dbHeaders:
    print(config['NameHeaderInCSV'])
