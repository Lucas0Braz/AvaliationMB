import sentry_sdk
from flask import Flask
from sentry_sdk.integrations.flask import FlaskIntegration

from flask import Flask
from flask_restful import Api

from resources.user import UserRegister
from resources.item import Item,ItemList
from resources.store import Store,StoreList

from db import db

#resource == stuffs that your api can return

sentry_sdk.init(
    dsn="https://1434eb02d33a449b93cc4f2be75c79b1@o483627.ingest.sentry.io/5536196",
    integrations=[FlaskIntegration()],
    traces_sample_rate=1.0
)


app = Flask(__name__)
db.init_app(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' #you can change the sqlite to any other db, the
#///means that we are in the root foulder of our project
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'llb'
api = Api(app)


api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')# the name is coming from get name
api.add_resource(ItemList, '/items')



app.run(port=5000, debug=False)