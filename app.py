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


def init_db_from_schema(app):
    """Initializes the database by executing the schema.sql file."""
    with app.app_context():
        # Ensure the path to schema.sql is correct
        schema_path = os.path.join(app.root_path, "data/schema.sql")
        if not os.path.exists(schema_path):
            print(
                f"Warning: schema.sql not found at {schema_path}. Skipping schema initialization."
            )
            return

        with open(schema_path, "r") as f:
            schema_sql = f.read()
            print(schema_sql)
        try:
            print("Executing schema.sql...")
            db.session.execute(text(schema_sql))
            db.session.commit()  # Commit the changes
            print("schema.sql executed successfully.")
        except Exception as e:
            db.session.rollback()  # Rollback in case of error
            print(f"Error executing schema.sql: {e}")


if __name__ == "__main__":
    app = create_app()
    init_db_from_schema(app)
    # To create tables, you might want to uncomment these lines once your models are defined
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
