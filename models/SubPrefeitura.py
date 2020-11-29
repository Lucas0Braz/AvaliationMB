from db import db
import sys

#todo subprefeitura
class SubPrefeituraModel(db.Model):
    __tablename__ = 'SubPrefeituras'

    id = db.Column(db.Integer, primary_key=True)
    adress = db.Column(db.String(300))
    #items = db.relationship('ItemModel', lazy='dynamic')


    def __init__(self, name):
        self.name = name

    def json(self):
        return {'id': self.id, 'name': self.name, 'items': [item.json() for item in self.items.all()]}

    @classmethod
    def search_store(cls, name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def search_store_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
