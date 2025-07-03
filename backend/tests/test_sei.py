from app.models import User
from app.extensions import db
from app.services.sei_client import SEIClient


def create_user():
    user = User(
        username="testuser",
        email="test@example.com",
        administrador=False,
        cpf="12345678909",
    )
    user.set_password("password")
    user.usuario_sei = "seiuser"
    user.set_senha_sei("senha")
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


def test_sei_login_calls_client(client, app, monkeypatch):
    with app.app_context():
        create_user()
    token = get_token(client)

    captured = {}

    def fake_init(self, session=None):
        pass

    def fake_login(self, usuario, senha, tok):
        captured["u"] = usuario
        captured["s"] = senha
        captured["t"] = tok

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(SEIClient, "login", fake_login)

    response = client.post(
        "/api/sei/login",
        json={"usuario": "seiuser", "senha_sei": "senha", "token_sei": "123"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert captured == {"u": "seiuser", "s": "senha", "t": "123"}


def test_sei_login_missing_fields(client, app):
    with app.app_context():
        create_user()
    token = get_token(client)

    response = client.post(
        "/api/sei/login",
        json={},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 400
