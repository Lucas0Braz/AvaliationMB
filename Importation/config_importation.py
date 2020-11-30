
from models.FeiraLivreModel import FeiraLivreModel
from models.Location import LocationModel
from models.Bairro import BairroModel
from models.Distrito import DistritoModel
from models.SubPrefeitura import SubPrefeituraModel
from models.SubRegiao import SubRegiaoModel
from models.Regiao import RegiaoModel


#todo get expected_type from obj_sqlAlchemy: sqlalchemy_utils.get_type(FeriaLivreModel.id)
#The order here is important,because will insert each one according to the index
dict_crossCsvHeader2dbHeaders = [
    {'NameHeaderInCSV': 'REGIAO5', 'expected_type': str, 'obj_sqlAlchemy': RegiaoModel.name},
    {'NameHeaderInCSV': 'REGIAO8', 'expected_type': str, 'obj_sqlAlchemy': SubRegiaoModel.name},
    {'NameHeaderInCSV': 'CODSUBPREF', 'expected_type': int, 'obj_sqlAlchemy': SubPrefeituraModel.id},
    {'NameHeaderInCSV': 'SUBPREFE', 'expected_type': str, 'obj_sqlAlchemy': SubPrefeituraModel.name},
    {'NameHeaderInCSV': 'CODDIST', 'expected_type': int, 'obj_sqlAlchemy': DistritoModel.id},
    {'NameHeaderInCSV': 'DISTRITO', 'expected_type': str, 'obj_sqlAlchemy': DistritoModel.name},
    {'NameHeaderInCSV': 'BAIRRO', 'expected_type': str, 'obj_sqlAlchemy': BairroModel.name},
    {'NameHeaderInCSV': 'ID', 'expected_type': int, 'obj_sqlAlchemy': FeiraLivreModel.id},
    {'NameHeaderInCSV': 'LONG', 'expected_type': float, 'obj_sqlAlchemy': LocationModel.long },
    {'NameHeaderInCSV': 'LAT', 'expected_type': float, 'obj_sqlAlchemy': LocationModel.lat },
    {'NameHeaderInCSV': 'SETCENS', 'expected_type': int, 'obj_sqlAlchemy': LocationModel.setor_cens},
    {'NameHeaderInCSV': 'AREAP', 'expected_type': int, 'obj_sqlAlchemy': LocationModel.area_pond},
    {'NameHeaderInCSV': 'LOGRADOURO', 'expected_type': str, 'obj_sqlAlchemy': LocationModel.endereco},
    {'NameHeaderInCSV': 'NUMERO', 'expected_type': str, 'obj_sqlAlchemy': LocationModel.numero},
    {'NameHeaderInCSV': 'REFERENCIA', 'expected_type': str, 'obj_sqlAlchemy': LocationModel.reference},
    {'NameHeaderInCSV': 'NOME_FEIRA', 'expected_type': str, 'obj_sqlAlchemy': FeiraLivreModel.name_feira},
    {'NameHeaderInCSV': 'REGISTRO', 'expected_type': str, 'obj_sqlAlchemy': FeiraLivreModel.cod_registro},



]





