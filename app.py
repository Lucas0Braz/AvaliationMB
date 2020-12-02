import sys
from flask import Flask, _app_ctx_stack
from flask_restful_swagger_3 import Api


import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sqlalchemy.orm import scoped_session

from resources.FeiraLivre import FeiraLivre
from resources.FeirasLivres import FeiraList
from ApiDocumentation import Contact
from db import SessionLocal, engine
from models import Base

Base.metadata.create_all(bind=engine)

app = Flask(__name__)
app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)
Base.session = app.session

Base.query = app.session.query_property()
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


api.add_resource(FeiraLivre, '/feira-livre/<string:codigo>')
api.add_resource(FeiraList, '/feira-list/<string:name>')



app.run(port=5000, debug=False)