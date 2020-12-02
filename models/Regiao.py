import sqlalchemy as db
from sqlalchemy.orm import relationship
from db import Base

class RegiaoModel(Base):
    __tablename__ = 'Regioes'

    name = db.Column(db.String(100), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    sub_regioes = relationship('SubRegiaoModel', backref='sub_regiao', lazy='dynamic')


    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name, 'sub_regioes': [sub_regiao.json() for sub_regiao in self.sub_regioes.all()]}

    @classmethod
    def search_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def search_regiao_id(cls, id):
        return cls.query.filter_by(id=id).first()


