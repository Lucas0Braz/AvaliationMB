from db import Base
from sqlalchemy.orm import relationship
import sqlalchemy as db

class FeiraLivreModel(Base):

    __tablename__ = 'FeirasLivres'

    id = db.Column(db.Integer, primary_key=True)
    cod_registro = db.Column(db.String(7), nullable=False)
    name_feira = db.Column(db.String(120), nullable=False)
    location_id = db.Column(db.String, db.ForeignKey('Localizacoes.id'), nullable=False)
    location = relationship("LocationModel", uselist=False, backref="Localizacoes", cascade="all, delete")

    def __init__(self, name_feira, cod_registro, location_id):
        self.name_feira = name_feira
        self.cod_registro = cod_registro
        self.location_id = location_id


    def json(self):
        return {'id': self.id, 'name_feira': self.name_feira, 'cod_registro': self.cod_registro, 'location': self.location.json_children() }

    @classmethod
    def search_feira_by_codigo(cls, cod_registro):

        return cls.query.filter_by(cod_registro=cod_registro).first()

    def search_feiras_by_name(cls, name):
        return cls.query.filter(name_feira=name)

    def save_to_db(self):
        Base.session.add(self)
        Base.session.commit()

    def delete_from_db(self):
        Base.session.delete(self)
        Base.session.commit()
