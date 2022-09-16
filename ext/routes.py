from datetime import datetime
from http.client import BAD_REQUEST
from .model import Usuario, Agendamento
from ext import login_maneger, db
from flask import render_template, request, redirect, url_for, flash, session
from flask_login import UserMixin, login_required, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


def init_app(app):
    
    @app.before_first_request
    def create_db():
        db.create_all()

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
            session['usuario'] = usuario.id
            if usuario and check_password_hash(usuario.senha, senha):
                login_user(usuario)
                if usuario.in_admin == 1:
                    return redirect (url_for('dash_admin', id=usuario.id))
                elif usuario.in_colaborador == 1:
                    return redirect (url_for('dash_colaborador', id=usuario.id))
                else:
                    return redirect(url_for('dash_cliente', id=usuario.id))
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
            user.in_admin = 0
            user.in_colaborador = 0
            user.in_ativo = 1
            
            db.session.add(user)
            db.session.commit()
            
            return redirect(url_for('login'))
        else:
            return BAD_REQUEST
    
    @app.route('/dashboard/<id>', methods=['GET', 'POST'])
    @login_required
    def dash_cliente(id):
        usuario = Usuario.query.filter_by(id = id).first()
        agendamentos = Agendamento.query.filter_by(id = id).count()
        if usuario.in_colaborador == 0:
            return render_template('dash_cliente/dashboard_cliente.html', usuario=usuario.nome)
        else:
            return BAD_REQUEST
        
    
    @app.route('/dashboard_colaborador/<id>', methods=['GET', 'POST'])
    @login_required
    def dash_colaborador(id):
        usuario = Usuario.query.filter_by(id = id).first()
        if usuario.in_colaborador == 1:
            agendamentos =  Agendamento.query.count()
            return render_template('dash_colaborador/dashboard_colaborador.html', agendamentos=agendamentos)
        else:
            return BAD_REQUEST
    
    @app.route('/dashboard_admin/<id>', methods=['GET', 'POST'])
    @login_required
    def dash_admin(id):
        usuario = Usuario.query.filter_by(id = id).first()
        agendamentos = Agendamento.query.filter_by().count()
        novos_usuarios = Usuario.query.filter_by().count()
        if usuario.in_admin == 1:
            return render_template('dash_admin/dashboard_admin.html',
                           novos_usuarios=novos_usuarios,
                           agendamentos=agendamentos)
        else:
            return BAD_REQUEST
 
    @app.route('/logout', methods=['GET', 'POST'])
    @login_required
    def logout():
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/agendamento', methods=['GET', 'POST'])
    @login_required
    def agendamento():
        if request.method == 'GET':
            return render_template('dash_cliente/agendamentos_cliente.html')
        elif request.method == 'POST':
            agendamento = Agendamento()
            agendamento.id_usuario = session['usuario']
            agendamento.nome = f'{request.form["nome"]} {request.form["sobrenome"]}'
            agendamento.email = request.form['email']
            agendamento.fone = request.form['telefone']
            agendamento.data_agendamento = request.form['dt_agendamento']
            agendamento.horario_agendamento = request.form['hr_agendamento']
            agendamento.colaborador = request.form['cabeleleiro']
            agendamento.data_registro = datetime.now()
            
            db.session.add(agendamento)
            db.session.commit()
            return render_template('dash_cliente/agendamentos_cliente.html')
        else:
            return BAD_REQUEST
     
        
    @app.route('/agendamento_editar/<id>', methods=['GET', 'POST'])
    @login_required
    def agendamento_editar(id):
        if request.method == 'GET':
            agendamento = Agendamento.query.filter_by(id=id).all()
            return render_template('dash_colaborador/agendamentos_colaborador.html', agendamento=agendamento)
        elif request.method == 'POST':
            agendamento = Agendamento.query.filter_by(id=id).first()
            # agendamento.id_usuario = session['usuario']
            agendamento.nome = request.form["nome"]
            agendamento.email = request.form['email']
            agendamento.fone = request.form['telefone']
            agendamento.data_agendamento = request.form['dt_agendamento']
            agendamento.horario_agendamento = request.form['hr_agendamento']
            agendamento.colaborador = request.form['cabeleleiro']
            agendamento.in_confimado = ( 1 if request.form['confirmado'] else 0)
            agendamento.in_realizado = ( 1 if request.form['in_realizado'] else 0)
            agendamento.data_registro = datetime.now()
            
            db.session.add(agendamento)
            db.session.commit()
            return render_template('dash_colaborador/agendamentos_colaborador.html')
        else:
            return BAD_REQUEST
        
    @app.route('/agendamento_finalizado/<id>', methods=['GET'])
    @login_required
    def agendamento_finalizado(id):
        agendamento = Agendamento.query.filter_by(id=id).first()
        agendamento.in_realizado = 1
         
        db.session.add(agendamento)
        db.session.commit()
        id_usuario = session['usuario']
        return redirect(url_for('dash_colaborador', id=id_usuario))
         

    @app.route('/lista_agendamentos', methods=['GET', 'POST'])
    @login_required
    def lista_agendamentos():
        if 'usuario' in session:
            id_usuario = session['usuario']
            usuario = Usuario.query.filter_by(id = id_usuario).first()
            if usuario.in_admin == 1:
                return render_template('lista_agendamentos_admin.html', lista_agendamentos=lista_agendamentos)
            elif usuario.in_colaborador == 1:
                lista_agendamentos = Agendamento.query.all()
                return render_template('dash_colaborador/listar_agendamentos_colaborador.html', lista_agendamentos=lista_agendamentos)
            else:
                lista_agendamentos = Agendamento.query.filter_by(id_usuario=id_usuario).all()
                return render_template('dash_cliente/lista_agendamentos_cliente.html', lista_agendamentos=lista_agendamentos)

