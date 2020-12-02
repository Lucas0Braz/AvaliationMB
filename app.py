import sys
from flask import Flask
from flask_restful_swagger_3 import Api


import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


from resources.FeiraLivre import FeiraLivre
from resources.FeirasLivres import FeiraList
from ApiDocumentation import Contact
from db import db, url_db


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = url_db
db.init_app(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'llb'
api = Api(app,
    contact=Contact.dict_contact,
    title='MercadoBitcoinAvaliacao',
    version=0.1
          )


sentry_sdk.init(
    dsn="https://1434eb02d33a449b93cc4f2be75c79b1@o483627.ingest.sentry.io/5536196",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)
@app.before_first_request
def prepare_api():
    #db.cre
    print('before all', file=sys.stderr)
    path2db = app.config['SQLALCHEMY_DATABASE_URI']
    path2csv = './DEINFO_AB_FEIRASLIVRES_2014.csv'
    db.create_all()


api.add_resource(FeiraLivre, '/feira-livre/<string:codigo>')
api.add_resource(FeiraList, '/feira-list/<string:name>')



app.run(port=5000, debug=False)