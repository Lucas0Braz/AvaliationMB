from db import db



class FeiraLivreModel(db.Model):
    __tablename__ = 'FeirasLivres'

    cod_registro = db.Column(db.String(7), primary_key=True)
    name_feira = db.Column(db.String(120), nullable=False)
    location_id = db.Column(db.String, db.ForeignKey('Localizacoes.id'), nullable=False)
    location = db.relationship("LocationModel", uselist=False, backref="Localizacoes")

    def __init__(self, name_feira, cod_registro, location):
        self.name_feira = name_feira
        self.cod_registro = cod_registro
        self.location = location

    def json(self):
        return {'name_feira': self.name_feira, 'cod_registro': self.cod_registro, 'location': self.location.json_children() }

    @classmethod
    def search_feira(cls, name):
        return cls.query.filter_by(name_feira=name).first()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
