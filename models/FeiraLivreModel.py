from db import db
from models.Location import LocationModel
import sys


class FeiraLivreModel(db.Model):
    __tablename__ = 'FeirasLivres'


    cod_registro = db.Column(db.String(7), primary_key=True)
    name_feira = db.Column(db.String(120))
    #location_id = db.Column(db.Integer, db.ForeignKey('location.id'))
    #location = db.relationship("LocationModel", back_populates="localizacoes", uselist=False)
    location = db.relationship("LocationModel", uselist=False, backref="localizacoes")

    def __init__(self, name_feira, cod_registro, location):
        self.name_feira = name_feira
        self.cod_registro = cod_registro
        #self.price = price
        self.location = location
        #self.store_id = store_id

    def json(self):

        return {'name': self.name, 'price': self.price, 'store_id': self.store_id, }

    @classmethod
    def search_feira(cls, name):
        return cls.query.filter_by(name_feira=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
