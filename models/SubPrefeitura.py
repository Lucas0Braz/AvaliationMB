import sqlalchemy as db
from sqlalchemy.orm import relationship
from db import Base
from models.SubRegiao import SubRegiaoModel as sub_regiao



class SubPrefeituraModel(Base):
    __tablename__ = 'SubPrefeituras'


    id = db.Column(db.Integer, primary_key=True, autoincrement=False)
    name = db.Column(db.String(100), nullable=False)
    distrito = relationship('DistritoModel', backref='distr', lazy='dynamic')

    sub_regiao_id = db.Column(db.Integer, db.ForeignKey('SubRegioes.id'), nullable=False)


    def __init__(self, id,sub_regiao_id, name):
        self.name = name
        self.sub_regiao_id = sub_regiao_id
        self.id = id


    def json_endpoint(self):
        ParentSub_regiao = sub_regiao.search_sub_regiao_id (self.sub_regiao_id).name
        return {'id': self.id, 'name': self.name,
                'sub_regiao': f'{ParentSub_regiao}',
                'distritos': f'{[distrito.json_children() for distrito in self.distrito.all()]}'}

    def json_children(self):
        ParentSub_regiao = sub_regiao.search_sub_regiao_id (self.sub_regiao_id).json_children()
        return {'id': self.id, 'name': self.name,
                'sub_regiao': ParentSub_regiao,
                }

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def search_sub_prefeitura_id(cls, id):
        return cls.query.filter_by(id=id).first()

