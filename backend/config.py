import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "jdeiie760zxzxfd$$#2*kkkdytsa")

    # Use an explicit, project-local path for the SQLite DB so agents and
    # developers don't end up reading/writing different files depending on
    # the current working directory. The file lives at `backend/instance/database.db`.
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = (
        os.getenv("DATABASE_URL")
        or f"sqlite:///{os.path.join(BASEDIR, 'instance', 'database.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Alterar em produção!!!
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "kdjkjfuirahfahuiiah&$hfhffh054545#")
    JWT_ACCESS_TOKEN_EXPIRES = False  # Alterar em produção!!!
    CHROMEDRIVER_PATH = os.getenv("CHROMEDRIVER_PATH")  # ⚠️ Aqui está o segredo
