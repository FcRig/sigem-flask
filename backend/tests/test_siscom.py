from app.extensions import db
from app.models import User
from app.routes.siscom import ENDPOINT
import requests


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

    class FakeResponse:
        status_code = 200
        content = b"data"

        def json(self):
            return payload

        def raise_for_status(self):
            pass

    def fake_get(url):
        assert url == f"{ENDPOINT}/123"
        return FakeResponse()

    monkeypatch.setattr(requests, "get", fake_get)

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
