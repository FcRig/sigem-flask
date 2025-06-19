import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "jdeiie760zxzxfd$$#2*kkkdytsa")
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Alterar em produção!!!
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "kdjkjfuirahfahuiiah&$hfhffh054545#")
    JWT_ACCESS_TOKEN_EXPIRES = False  # Alterar em produção!!!
    CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")  # ⚠️ Aqui está o segredo
