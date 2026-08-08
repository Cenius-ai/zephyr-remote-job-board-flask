import os


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "cenius-dev-a3f7b2c1d4e5f6a8")
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JOBS_PER_PAGE = 12
