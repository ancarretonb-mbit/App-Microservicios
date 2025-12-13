from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .config import Config

# Crear motor de SQLAlchemy con puerto
engine = create_engine(
    f"mysql+pymysql://{Config.MYSQL_USER}:{Config.MYSQL_PASSWORD}@{Config.MYSQL_HOST}:{Config.MYSQL_PORT}/{Config.MYSQL_DB}"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_app():
    app = Flask(__name__)
    app.config['MYSQL_DB'] = Config.MYSQL_DB
    app.session = SessionLocal

    from .routes import routes_bp
    app.register_blueprint(routes_bp)

    return app

