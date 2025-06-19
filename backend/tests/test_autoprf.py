from app.extensions import db
from app.models import User
from app.utils.autoprf import AutoPRFClient

from flask_jwt_extended import create_access_token


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


def test_autoprf_login_stores_session(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        cpf_value = user.cpf

    def fake_login(self, cpf, password, token):
        assert cpf == cpf_value
        assert password == "autoprf-pass"
        assert token == "123456"
        return "cookie=value"

    def fake_init(self):
        self.driver = None

    monkeypatch.setattr(AutoPRFClient, "__init__", fake_init)
    monkeypatch.setattr(AutoPRFClient, "login", fake_login)

    token = get_token(client)
    response = client.post(
        "/api/autoprf/login",
        json={"password": "autoprf-pass", "token": "123456"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    with app.app_context():
        updated = User.query.get(user.id)
        assert updated.autoprf_session == "cookie=value"
