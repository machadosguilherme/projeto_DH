from flask_sqlalchemy import SQLAlchemy
from ext import db
from flask_login import UserMixin


class Usuario(db.Model, UserMixin):
    __tablename__ = "USUARIOS"
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(length=255), nullable=False)
    rua = db.Column(db.String(length=255), nullable=False)
    numero = db.Column(db.String(length=10), nullable=False)
    bairro = db.Column(db.String(length=255), nullable=False)
    cidade = db.Column(db.String(length=255), nullable=False)
    estado = db.Column(db.String(length=255), nullable=False)
    fone = db.Column(db.String(length=50), nullable=False)
    email = db.Column(db.String(length=255), nullable=False, unique=True, index=True)
    senha = db.Column(db.String(length=200), nullable=False)
    in_ativo = db.Column(db.Boolean)
    in_colaborador = db.Column(db.Boolean)
    in_admin = db.Column(db.Boolean)

    def __str__(self):
        return self.name