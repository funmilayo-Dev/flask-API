from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from config import Config

from flask_swagger_ui import get_swaggerui_blueprint

db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate()
SWAGGER_URL = '/api/docs' #URL for exposing SWAGGER UI (without trailing '/')
API_URL = 'http://127.0.0.1:5000'

def create_app(config=Config):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    migrate.init_app(app, db)
    ma.init_app(app)

    from w3w.views import api
    app.register_blueprint(api)


    with app.app_context():
        db.create_all()

    return app

# from app import views
