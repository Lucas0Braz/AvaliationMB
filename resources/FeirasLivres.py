from helperFuncs import clean_data_str

from flask_restful_swagger_3 import swagger, Resource
from models.FeiraLivreModel import FeiraLivreModel
from db import Base


class FeiraList(Resource):
    @swagger.tags(['feira-list'])
    @swagger.response(response_code=200, description='get all feiras with a given name')
    def get(self, name):
        name = clean_data_str(name).capitalize()
        result = [1,1]
        try:
            result = Base.session.query(FeiraLivreModel).filter(FeiraLivreModel.name_feira == name)
        except Exception as e:
            import sys
            print(repr(e), file=sys.stderr)
        all_feiras = [feira.json() for feira in result]
        if all_feiras == []:
            return {'message': 'no feiras with the name {}'.format(name)}

        return {'feiras': all_feiras}, 200
