import sys
import re
from flask_restful import reqparse
from flask_restful_swagger_3 import swagger, Resource

from models.FeiraLivreModel import FeiraLivreModel
from models.Location import LocationModel
from models.Regiao import RegiaoModel
from models.SubRegiao import SubRegiaoModel
from models.SubPrefeitura import SubPrefeituraModel
from models.Distrito import DistritoModel
from models.Bairro import BairroModel

from helperFuncs import clean_data_str



class FeiraLivre(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name_feira',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('latitude',
                        type=float,
                        required=True,
                        help="This field cannot be left blank and must be a float"
                        )
    parser.add_argument('longitude',
                        type=float,
                        required=True,
                        help="This field cannot be left blank and must be a float"
                        )
    parser.add_argument('setor_censitario',
                        type=int,
                        required=True,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('area_ponderada',
                        type=int,
                        required=True,
                        )
    parser.add_argument('endereco',
                        type=str,
                        required=True,
                        )
    parser.add_argument('numero',
                        type=str,
                        required=True,
                        )
    parser.add_argument('referencia',
                        type=str,
                        )
    parser.add_argument('bairro',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )


    @swagger.tags(['feira-livre'])
    @swagger.response(response_code=204, description='get an feira by cod_registro')
    def get(self, codigo):

        feira = FeiraLivreModel.search_feira_by_codigo(codigo)

        if feira:
            return feira.json()
        return {'message': f'feira with the {codigo} does not exist'}, 404

    @swagger.tags(['feira-livre'])
    @swagger.response(response_code=201, description='created feira')
    @swagger.reqparser(name='FeiraLivreModel', parser=parser)
    def post(self, codigo):
        data = FeiraLivre.parser.parse_args()
        codigo = clean_data_str(codigo)
        fields_validations = self.__fields_validation(data, codigo)
        if fields_validations != True:
            return fields_validations
        if len(data['endereco']) < 1:
            return {'endereco': 'this field {} can not be left blank'.format(data['endereco'])}, 400
        if FeiraLivreModel.search_feira_by_codigo(codigo) is not None:
            return {'message': 'the feira {} already exists'.format(codigo)}, 409
        feira = self.__create_feira(data, codigo)
        tup = ({}, 200)
        if type(feira) == type(tup):

            return feira

        return feira.json(), 201


    @swagger.tags(['feira-livre'])
    @swagger.response(response_code=204, description='delete an feira by cod_registro')
    def delete(self, codigo):
        feira = FeiraLivreModel.search_feira_by_codigo(codigo)

        if feira is None:
            return {'message': 'feira {} does not exist'.format(codigo)}, 400
        try:
            feira.delete_from_db()
        except Exception as e:
             print(f'at deleting an feira in db, the following error show up: {repr(e)}', file=sys.stderr)
             return {'message': 'feira {} has not been deleted'.format(codigo)}, 500

        return {'message': 'feira {} deleted'.format(codigo)}, 204

    @swagger.tags(['feira-livre'])
    @swagger.response(response_code=201, description='created feira')
    @swagger.reqparser(name='FeiraLivreModel', parser=parser)
    def put(self, codigo):
        data = FeiraLivre.parser.parse_args()
        codigo = clean_data_str(codigo)
        fields_validations = self.__fields_validation(data, codigo)
        if fields_validations != True:
            return fields_validations

        feira = self.__create_feira(data, codigo)
        tup = ({}, 200)
        if type(feira) == type(tup):
            print(f'{type(feira)} == {type(FeiraLivreModel)}', file=sys.stderr)
            return feira



        return feira.json()


    def __fields_validation(self, data, codigo):
        if len(data['name_feira']) > 120:
            return {'name_feira': 'can only have 120 caracteres'}, 400
        if len(str(data['setor_censitario'])) != 15:
            return {'setor_censitario': 'this field {} must be an int with 15 digits'.format(data['setor_censitario'])}, 400
        if len(str(data['area_ponderada'])) != 13:
            return {'area_ponderada': 'the area_ponderada {} must be an int with 13 digits'.format(data['area_ponderada'])}, 400
        if re.search(r'^[-]*\d+\.\d+$', str(data['latitude'])) is None:
            return {'latitude': 'this field must be an float with the latitude'}, 400
        if re.search(r'^[-]*\d+\.\d+$', str(data['longitude'])) is None:
            return {'longitude': 'this field must be an float with the longitude'}, 400
        if data['latitude'] > 90 or data['latitude'] < -90:
            return {'latitude': 'must be beteween -90 and 90, not {}'.format(data['latitude'])}, 400
        if data['longitude'] > 180 or data['longitude'] < -180:
            return {'longitude': 'must be beteween -180 and 180, not {}'.format(data['longitude'])}, 400
        if re.search(r'^\d+[-]{1}\d+$', codigo) is None:
            return {'cod_registro': 'the cod_registro in the url {} must follow the pattern: "1234-6"'.format(codigo)}, 400

        return True

    def __create_feira(self, data, codigo):
        bairro = clean_data_str(data['bairro']).capitalize()
        bairro_model = BairroModel.search_by_name(bairro)

        if bairro_model is None:
            return {'message': 'the bairro {} does not exists in our data base'.format(bairro)}, 400

        dict_location = {'lat': data['latitude'], 'long': data['longitude'],
                         'setor_cens': data['setor_censitario'], 'area_pond': data['area_ponderada'],
                         'endereco': clean_data_str(data['endereco']), 'numero': clean_data_str(data['numero']),
                         'referencia': clean_data_str(data['referencia']), 'bairro_id': bairro_model.id}
        location_model = LocationModel(**dict_location)
        try:
            location_model.save_to_db()
        except Exception as e:
            print(f'at saving to db, the following error show up: {repr(e)}', file=sys.stderr)
            return {'message': 'Something has go wrong with internally '}, 500
        location_id = location_model.id

        data['name_feira'] = clean_data_str(data['name_feira']).capitalize()

        dict_feira = {'name_feira': data['name_feira'], 'cod_registro': codigo, 'location_id': location_id}
        feira = FeiraLivreModel(**dict_feira)
        try:
            feira.save_to_db()
        except Exception as e:
            print(f'at saving to db, the following error show up: {repr(e)}', file=sys.stderr)
            return {'message': 'Something has go wrong with internal api '}, 500
        return feira