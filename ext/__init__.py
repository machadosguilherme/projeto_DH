from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


db = SQLAlchemy()
Bootstrap()
login_maneger = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'teste12345'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///server.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    db.init_app(app)
    login_maneger.init_app(app)
    
    from ext import routes
    routes.init_app(app)
    
    return app