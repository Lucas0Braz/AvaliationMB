from db import Base
import sqlalchemy as db
from sqlalchemy.orm import relationship
from models.SubPrefeitura import SubPrefeituraModel as sub_prefeitura



class DistritoModel(Base):
    __tablename__ = 'Distritos'


    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(100), nullable=False)
    bairros = relationship('BairroModel', backref='bairro', lazy='dynamic')

    sub_prefeitura_id = db.Column(db.Integer, db.ForeignKey('SubPrefeituras.id'), nullable=False)


    def __init__(self, name,id,sub_prefeitura_id):
        self.name = name
        self.sub_prefeitura_id = sub_prefeitura_id
        self.id = id

    def json_endpoint(self):
        ParentSub_prefeitura = sub_prefeitura.search_sub_prefeitura_id(self.sub_prefeitura_id).name
        return {'id': self.id, 'name': self.name,
                'sub_prefeitura': f'{ParentSub_prefeitura}',
                'bairros': {[bairro.json_children() for bairro in self.bairros.all()]} }

    def json_children(self):
        ParentSub_prefeitura = sub_prefeitura.search_sub_prefeitura_id(self.sub_prefeitura_id).json_children()
        return {'id': self.id, 'name': self.name,
                'sub_prefeitura': ParentSub_prefeitura,
                }

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def search_distritos_id(cls, id):
        return cls.query.filter_by(id=id).first()

