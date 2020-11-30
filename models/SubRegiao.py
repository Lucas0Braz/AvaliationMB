from db import db
from models.Regiao import RegiaoModel as regiao



class SubRegiaoModel(db.Model):
    __tablename__ = 'SubRegioes'


    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    sub_prefeituras = db.relationship('SubPrefeituraModel', backref='subpref', lazy='dynamic')

    regiao_id = db.Column(db.Integer, db.ForeignKey('Regioes.id'), nullable=False)


    def __init__(self, id):
        self.id = id

    def json_endpoint(self):
        return {'id': self.id, 'name': self.name,
                'regiao': f'{regiao.search_regiao_id(self.regiao_id).name}',
                'sub_prefeituras': f'{[subprefeitura.json() for subprefeitura in self.sub_prefeituras.all()]}'}

    def json_children(self):
        return {'name': self.name,
                'regiao': f'{regiao.search_regiao_id(self.regiao_id).name}'}

    @classmethod
    def search_sub_regiao(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def search_sub_regiao_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
