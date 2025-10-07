import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

#CRIAÇÃO DO TOKEN
class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL") or \
        "sqlite:///" + os.path.join(BASE_DIR, "app.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = "super-secret-key" 
    
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)