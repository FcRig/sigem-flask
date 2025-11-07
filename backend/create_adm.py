from app import create_app
from app.extensions import db
from app.models import User
from werkzeug.security import generate_password_hash

app = create_app()

with app.app_context():
    user = User(
        username="leoadm",
        email="leoadm@gmail.com",
        password_hash=generate_password_hash("1234"),
        administrador=True
    )
    db.session.add(user)
    db.session.commit()
    print("Usuário admin criado com sucesso!")
