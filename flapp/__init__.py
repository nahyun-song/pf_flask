from flask import Flask, render_template, redirect, url_for, request, session, flash
from flapp.routes.main_route import bp as main_bp
from flapp.routes.sub_route import bp_app as sub_bp
from flapp.models import db, migrate, User, Keyword
import requests
from bs4 import BeautifulSoup

def create_app():
    app = Flask(__name__) 
    app.register_blueprint(main_bp)
    app.register_blueprint(sub_bp)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
    app.config['SECRET_KEY'] = '_5#y2L"F4Q8z\n\xec]/'

    with app.app_context(): 
        db.init_app(app) 
        migrate.init_app(app, db)

    return app


if __name__ == '__main__':
    app = create_app()
    db.create_all()
    app.run(debug=True)