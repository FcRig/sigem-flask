from .extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    administrador = db.Column(db.Boolean, default=False)
    cpf = db.Column(db.String(14), unique=True)
    senha_autoprf_hash = db.Column('senha_autoprf', db.String(120))
    autoprf_session = db.Column(db.Text)
    senha_siscom_hash = db.Column('senha_siscom', db.String(120))
    senha_sei_hash = db.Column('senha_sei', db.String(120))
    usuario_sei = db.Column(db.String(120))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_senha_autoprf(self, password):
        self.senha_autoprf_hash = generate_password_hash(password)

    def check_senha_autoprf(self, password):
        return check_password_hash(self.senha_autoprf_hash or '', password)

    def set_senha_siscom(self, password):
        self.senha_siscom_hash = generate_password_hash(password)

    def check_senha_siscom(self, password):
        return check_password_hash(self.senha_siscom_hash or '', password)

    def set_senha_sei(self, password):
        self.senha_sei_hash = generate_password_hash(password)

    def check_senha_sei(self, password):
        return check_password_hash(self.senha_sei_hash or '', password)
