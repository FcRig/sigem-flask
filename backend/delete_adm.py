from app import create_app
from app.extensions import db
from app.models import User  # se o arquivo for outro (ex: models.user), ajusta o import

app = create_app()

with app.app_context():
    user = User.query.filter_by(username="leoadm").first()
    if user:
        db.session.delete(user)
        db.session.commit()
        print("🗑️ Usuário 'leoadm' deletado com sucesso!")
    else:
        print("⚠️ Usuário 'leoadm' não encontrado.")
