import os
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "jdeiie760zxzxfd$$#2*kkkdytsa")
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "kdjkjfuirahfahuiiah&$hfhffh054545#")
