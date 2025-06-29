from app.extensions import db
from app.models import User
from app.routes.siscom import ENDPOINT
from app.services.siscom_client import SiscomClient


def create_user():
    user = User(
        username="testuser",
        email="test@example.com",
        administrador=False,
        cpf="12345678909",
    )
    user.set_password("password")
    db.session.add(user)
    db.session.commit()
    return user


def get_token(client, email="test@example.com", password="password"):
    response = client.post(
        "/api/auth/login",
        json={"email": email, "password": password},
    )
    assert response.status_code == 200
    return response.get_json()["access_token"]


def test_pesquisar_ai_returns_filtered_fields(client, app, monkeypatch):
    with app.app_context():
        create_user()

    token = get_token(client)

    payload = {
        "numeroAuto": "A1",
        "codigoInfracao": "123",
        "descAbreviadaInfracao": "desc",
        "placa": "ABC1234",
        "renavam": "999",
        "kmInfracao": "10",
        "municipioInfracao": {"nome": "Cidade"},
        "valorInfracao": 100.0,
        "extra": "ignored",
    }

    def fake_init(self, endpoint=None):
        assert endpoint == ENDPOINT
        self.endpoint = endpoint

    def fake_pesquisar(self, numero):
        assert numero == "123"
        return {k: payload[k] for k in payload if k != "extra"}

    monkeypatch.setattr(SiscomClient, "__init__", fake_init)
    monkeypatch.setattr(SiscomClient, "pesquisar_ai", fake_pesquisar)

    response = client.post(
        "/api/siscom/pesquisar_ai",
        json={"numero": "123"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.get_json() == {
        "numeroAuto": "A1",
        "codigoInfracao": "123",
        "descAbreviadaInfracao": "desc",
        "placa": "ABC1234",
        "renavam": "999",
        "kmInfracao": "10",
        "municipioInfracao": {"nome": "Cidade"},
        "valorInfracao": 100.0,
    }
