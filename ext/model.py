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

class Agendamento(db.Model):
    __tablename__ = "AGENDAMENTO"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('USUARIOS.id'))
    nome = db.Column(db.String(length=255), nullable=False)
    email = db.Column(db.String(length=255), nullable=False)
    fone = db.Column(db.String(length=50), nullable=False)
    data_agendamento = db.Column(db.String(length=10), nullable=False)
    horario_agendamento = db.Column(db.String, nullable=False)
    colaborador = db.Column(db.String)
    data_registro = db.Column(db.DateTime, nullable=False)
    in_confimado = db.Column(db.Boolean)
    in_realizado =db.Column(db.Boolean)
    id_usuario_finalizacao = db.Column(db.Integer, db.ForeignKey('USUARIOS.id'))

    def __str__(self):
        return self.name
