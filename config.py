import os

class Config:
    SECRET_KEY = "cmrl-secret-key"

    SQLALCHEMY_DATABASE_URI = "sqlite:///cmrl_portal.db"

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    UPLOAD_FOLDER = "uploads"

    MAX_CONTENT_LENGTH = 100 * 1024 * 1024