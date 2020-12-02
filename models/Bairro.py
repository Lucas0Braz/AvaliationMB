import sqlalchemy as db
from sqlalchemy.orm import relationship
from db import Base
from models.Distrito import DistritoModel



class BairroModel(Base):
    __tablename__ = 'Bairros'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    locations = relationship('LocationModel', backref='location', lazy='dynamic')

    distrito_id = db.Column(db.Integer, db.ForeignKey('Distritos.id'), nullable=False)


    def __init__(self, name):
        self.name = name

    def json_endpoint(self):
        ParentDistrito = DistritoModel.search_distritos_id(self.distrito_id).name
        return {'id': self.id, 'name': self.name,
                'distrito': f'{ParentDistrito}',
                'enderecos': {[location.json_children() for location in self.locations.all()]}}

    def json_children(self):
        ParentDistrito = DistritoModel.search_distritos_id(self.distrito_id).json_children()
        return {'id': self.id, 'name': self.name,
                'distrito': ParentDistrito,
                }

    @classmethod
    def search_bairro(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def search_bairro_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        Base.session.add(self)
        Base.session.commit()

    def delete_from_db(self):
        Base.session.delete(self)
        Base.session.commit()
