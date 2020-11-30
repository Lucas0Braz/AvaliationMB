from flask_restful import Resource, reqparse
from models.FeiraLivreModel import FeiraLivreModel
from models.Location import LocationModel
from models.Regiao import RegiaoModel
from models.SubRegiao import SubRegiaoModel
from models.SubPrefeitura import SubPrefeituraModel
from models.Distrito import DistritoModel
from models.Bairro import BairroModel




class FeiraLivre(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=False,
                        help="This field cannot be left blank"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=False,
                        help="All Items need an Store<StoreID>"
                        )

    def get(self, name):

        feira = FeiraLivreModel.search_feira(name)
        #sub_prefeitura = BairroModel.search_bairro(name)
        if feira:
            return feira.json()
        return {'message': 'item not found'}, 404

    def post(self, name):
        if FeiraLivreModel.search_feira(name) is not None:
            return {'message': 'the item {} already exists'.format(name)}, 400

        data = Item.parser.parse_args()

        if StoreModel.search_store_by_id(data['store_id']) is None:
            return {'message': 'the store {} does not exists'.format(data['store_id'])}, 400

        item = FeiraLivreModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'Something has go wrong at saving to db'}, 500

        return item.json(), 201

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

