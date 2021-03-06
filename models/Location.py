import sqlalchemy as db
from db import Base
from models.Bairro import BairroModel


class LocationModel(Base):
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

    def __init__(self, lat, long, setor_cens, area_pond, endereco, numero, referencia, bairro_id):
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
        return {'id': self.id, 'latitude': self.lat, 'long': self.long, 'setor_censitario': self.setor_cens,
                'area_ponderada': self.area_pond, 'endereco': self.endereco,
                'numero': self.numero, 'referencia': self.referencia,
                'bairro': ParentBairro }

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter_by(endereco=name).first()

    def search_by_lat_long(cls, lat, long):
        return cls.query.filter_by(lat=lat, long=long).first()

    @classmethod
    def search_location_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        Base.session.add(self)
        Base.session.commit()

    def delete_from_db(self):
        Base.session.delete(self)
        Base.session.commit()
