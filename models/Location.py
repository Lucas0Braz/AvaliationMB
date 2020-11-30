from db import db
from models.Bairro import BairroModel


class LocationModel(db.Model):
    __tablename__ = 'Localizacoes'

    id = db.Column(db.Integer, primary_key=True)
    lat = db.Column(db.FLOAT(precision=32, decimal_return_scale=None))
    long = db.Column(db.FLOAT(precision=32, decimal_return_scale=None))
    setor_cens = db.Column(db.Integer(), nullable=False)
    area_pond = db.Column(db.Integer(), nullable=False)
    endereco = db.Column(db.String(300), nullable=False)
    numero = db.Column(db.String(10), nullable=False)
    referencia = db.Column(db.String(300))

    bairro_id = db.Column(db.Integer, db.ForeignKey('Bairros.id'), nullable=False)

    def __init__(self,lat, long, setor_cens, area_pond, endereco, numero, referencia, bairro_id):
        self.lat = lat
        self.long = long
        self.setor_cens = setor_cens
        self.area_pond = area_pond
        self.endereco = endereco
        self.numero = numero
        self.referencia = referencia
        self.bairro_id = bairro_id

    def json_children(self):
        ParentBairro = BairroModel.search_bairro_id(self.bairro_id).json_children()
        return {'id': self.id, 'long': self.long,
                'bairro': ParentBairro }

    @classmethod
    def search_location(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def search_location_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
