from flask import Flask
from .extensions import db, migrate, jwt, cors
from .routes import auth, scraping, autoprf

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

    return app
