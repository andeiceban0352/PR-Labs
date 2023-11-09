# app.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models.database import db
from models.electro_scooter import ElectroScooter
from flasgger import Swagger

def create_app():
    app = Flask(__name__)
    # Configure SQLAlchemy to use SQLite
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://andrei:123123@localhost/your_database.db'  

    db.init_app(app)
    Swagger(app)
    return app

if __name__ == "__main__":
    app = create_app()
    import routes
    app.run(host='127.0.0.1', port=96)