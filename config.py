import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "a_fallback_secret_key_for_development"

    # Database Configuration
    # Get MySQL connection details from environment variables
    MYSQL_HOST = os.environ.get("MYSQL_HOST") or "localhost"
    MYSQL_PORT = os.environ.get("MYSQL_PORT") or "3306"  # Ensure it's a string
    MYSQL_USER = os.environ.get("MYSQL_USER") or "root"  # Default for local MySQL
    MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD") or ""  # Default for local MySQL
    MYSQL_DB = os.environ.get("MYSQL_DB") or "default_db"

    # Construct the SQLAlchemy Database URI
    # Using 'mysql+pymysql' dialect for PyMySQL connector
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@"
        f"{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Suppress warning and save memory
