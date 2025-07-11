from flask import Flask
from .extensions import db, migrate, jwt, cors
from .routes import auth, scraping, autoprf, siscom, veiculo, sei

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    cors.init_app(app)

    app.register_blueprint(auth.bp)
    app.register_blueprint(scraping.bp)
    app.register_blueprint(autoprf.bp)
    app.register_blueprint(siscom.bp)
    app.register_blueprint(veiculo.bp)
    app.register_blueprint(sei.bp)

    return app
