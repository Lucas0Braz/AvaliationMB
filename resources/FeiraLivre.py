import sys
import re
from flask_restful import Resource, reqparse


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
    parser.add_argument('cod_registro',
                        type=str,
                        required=True,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('name_feira',
                        type=str,
                        required=False,
                        help="All Feiras must have a name"
                        )
    parser.add_argument('latitude',
                        type=float,
                        required=False,
                        help="You need the latitude"
                        )
    parser.add_argument('longitude',
                        type=float,
                        required=False,
                        help="Longitude will only accept floats"
                        )
    parser.add_argument('setor_censitario',
                        type=int,
                        required=False,
                        help=""
                        )
    parser.add_argument('area_ponderada',
                        type=int,
                        required=False,
                        )
    parser.add_argument('endereco',
                        type=str,
                        required=False,
                        )
    parser.add_argument('numero',
                        type=str,
                        required=False,
                        )
    parser.add_argument('referencia',
                        type=int,
                        required=False,
                        )
    parser.add_argument('bairro',
                        type=str,
                        required=True,
                        help="Bairro is necessary for retrieving all data"
                        )


    def get(self, codigo):

        feira = FeiraLivreModel.search_feira_by_codigo(codigo)

        if feira:
            return feira.json()
        return {'message': f'feira with the {codigo} does not exist'}, 404

    def post(self, codigo):
        data = FeiraLivre.parser.parse_args()
        if data['latitude'] > 90 or data['latitude'] < -90:
            return {'message': 'the latitude {} must be beteween -90 and 90'.format(data['latitude'])}, 400
        if data['longitude'] > 180 or data['longitude'] < -180:
            return {'message': 'the longitude {} must be beteween -180 and 180'.format(data['longitude'])}, 400
        if len(data['endereco']) < 1:
            return {'message': 'the endereco {} can not be left blank'.format(data['endereco'])}, 400
        if len(str(data['setor_censitario'])) != 15:
            return {'message': 'the setor_censitario {} must be 15 digits'.format(data['setor_censitario'])}, 400
        if len(str(data['area_ponderada'])) != 14:
            return {'message': 'the area_ponderada {} must be 14 digits'.format(data['area_ponderada'])}, 400
        if FeiraLivreModel.search_feira_by_codigo(codigo) is not None:
            return {'message': 'the feira {} already exists'.format(codigo)}, 400


        bairro = clean_data_str(data['bairro']).capitalize()
        bairro_model = BairroModel.search_bairro(bairro)

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
            return {'message': 'Something has go wrong with internal api '}, 500
        location_id = location_model.id

        data['name_feira'] = clean_data_str(data['name_feira']).capitalize()
        data['cod_registro'] = clean_data_str(data['cod_registro'])
        if re.search(r'^\d+-\d+^$', data['cod_registro']) is None:
            return 'the cod_registro {} must follow the pattern: "1234-6"'.format(data['cod_registro']), 400

        dict_feira = {'name_feira': data['name_feira'], 'cod_registro': data['cod_registro'], 'location_id': location_id}
        feira = FeiraLivreModel(**dict_feira)

        try:
            feira.save_to_db()
        except Exception as e:
            print(f'at saving to db, the following error show up: {repr(e)}', file=sys.stderr)
            return {'message': 'Something has go wrong with internal api '}, 500

        return feira.json(), 201

    def delete(self, name):
        item = FeiraLivreModel.search_item(name)
        if item:
            item.delete_from_db()
        return {'message': 'item deleted'}

    def put(self, name):
        data = Item.parser.parse_args()

        item = FeiraLivreModel.search_item(name)

        if item is None:
            item = FeiraLivreModel(name, **data)

        else:
            item.price = data['price']
            item.store_id = data['store_id']

        if StoreModel.search_store_by_id(data['store_id']) is None:
            return {'message': 'the store {} does not exists'.format(data['store_id'])}, 400

        item.save_to_db()
        return item.json()

