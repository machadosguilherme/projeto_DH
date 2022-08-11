from http.client import BAD_REQUEST
from .model import Usuario
from ext import login_maneger, db
from flask import render_template, request, redirect, url_for, flash
from flask_login import UserMixin, login_required, login_user
from werkzeug.security import generate_password_hash, check_password_hash


def init_app(app):

    @login_maneger.user_loader
    def current_user(id):
        return Usuario.query.get(id)

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'GET':
            return render_template('login-v2.html')
        elif request.method == 'POST':
            email = request.form['email']
            senha = request.form['senha']
            usuario = Usuario.query.filter_by(email=email).first()
            if usuario and check_password_hash(usuario.senha, senha):
                login_user(usuario)
                return #TODO Dashboard
            else:
                flash('Credências Invalidas.')
                return redirect(url_for('login'))
        else:
            return BAD_REQUEST

    @app.route('/cadastrar', methods=['GET', 'POST'])
    def cadastrar():
        if request.method == 'GET':
            return render_template('cadastro.html')
        elif request.method == 'POST':
            user = Usuario()
            user.nome = request.form['nome']
            user.rua = request.form['rua']
            user.numero = request.form['numero']
            user.bairro = request.form['bairro']
            user.cidade = request.form['cidade']
            user.estado = request.form['estado']
            user.fone = request.form['fone']
            user.email = request.form['email']
            user.senha = generate_password_hash(request.form['senha'])
            
            db.session.add(user)
            db.session.commit()
            
            return redirect(url_for('login'))
        else:
            return BAD_REQUEST
        