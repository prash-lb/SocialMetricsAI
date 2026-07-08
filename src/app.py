import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # <--- Add this import
from sqlalchemy import text

from routes import api_bp  # Keep this if you modified it as per previous instructions

db = SQLAlchemy()  # <--- Initialize SQLAlchemy here


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")  # Load configuration from config.py

    db.init_app(app)  # <--- Initialize the database with the Flask app

    app.register_blueprint(api_bp, url_prefix="/api")
    return app


if __name__ == "__main__":
    app = create_app()
    # init_db_from_schema(app)
    # To create tables, you might want to uncomment these lines once your models are defined
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
