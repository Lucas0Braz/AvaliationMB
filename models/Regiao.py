from db import db

class RegiaoModel(db.Model):
    __tablename__ = 'Regioes'

    name = db.Column(db.String(100), nullable=False)
    id = db.Column(db.Integer, primary_key=True)
    sub_regioes = db.relationship('SubRegiaoModel', backref='sub_regiao', lazy='dynamic')


    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name, 'sub_regioes': [sub_regiao.json() for sub_regiao in self.sub_regioes.all()]}

    @classmethod
    def search_regiao(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def search_regiao_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
