from flask import Flask
from pymongo import MongoClient
from app.models.station import Station
from app.models.user import User
from app.controllers.station_controller import station_controller
from app.controllers.user_controller import user_controller
from dotenv import load_dotenv
import os
from app.swagger import api

def create_app():
    app = Flask(__name__)

    load_dotenv()

    app.config['GOOGLE_MAP_API_KEY'] = os.getenv('GOOGLE_MAP_API_KEY', 'test')
    app.config['DATABASE_URL'] = os.getenv('DATABASE_URL', 'mongodb://localhost:27017')

    database_url = app.config['DATABASE_URL']
    
    if 'mongodb.net' in database_url:
        client = MongoClient(database_url, tls=True, tlsAllowInvalidCertificates=True)
    else:
        client = MongoClient(database_url)

    db = client['EVAT']

    app.charging_stations = Station(db)
    app.users = User(db)

    api.init_app(app)

    app.register_blueprint(station_controller)
    app.register_blueprint(user_controller)

    return app
