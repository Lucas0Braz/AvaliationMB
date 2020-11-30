from flask import Flask
from flask_restful import Api

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration


from resources.FeiraLivre import FeiraLivre


from db import db, url_db
import sys






app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = url_db
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'llb'
api = Api(app)

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

#api.add_resource(Store, '/store/<string:name>')
api.add_resource(FeiraLivre, '/feira-livre/<string:codigo>')# the name is coming from get name
#api.add_resource(ItemList, '/items')



app.run(port=5000, debug=False)