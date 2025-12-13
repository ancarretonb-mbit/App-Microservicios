import os

class Config:
    MYSQL_USER = os.getenv("MYSQL_USER", "mbit")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "mbit")
    MYSQL_HOST = os.getenv("MYSQL_HOST", "db")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))  # <-- convertir a int
    MYSQL_DB = os.getenv("MYSQL_DB", "mysql_pictures")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "app/uploads"
