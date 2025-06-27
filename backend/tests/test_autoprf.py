from app.extensions import db
from app.models import User
from app.services.autoprf_client import AutoPRFClient
import requests

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
        return "jwt-token"

    def fake_init(self, jwt_token=None):
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
        assert updated.autoprf_session == "jwt-token"

def test_pesquisar_ai_returns_data(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.autoprf_session = "sessao"
        db.session.commit()
        user_id = user.id

    token = get_token(client)

    expected = {
        "id": 99,
        "infracao": {"codigo_descricao": "desc"},
        "veiculo": {"placa": "ABC"},
        "local": {"codigo_municipio_uf": "000"},
    }

    def fake_init(self, jwt_token=None):
        assert jwt_token == "sessao"
        self.jwt_token = jwt_token

    def fake_pesquisa(self, numero):
        assert numero == "1234"
        return expected

    monkeypatch.setattr(AutoPRFClient, "__init__", fake_init)
    monkeypatch.setattr(AutoPRFClient, "pesquisa_auto_infracao", fake_pesquisa)

    response = client.post(
        "/api/autoprf/pesquisar_ai",
        json={"auto_infracao": "1234"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.get_json() == expected


def test_envolvidos_returns_list(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.autoprf_session = "sessao"
        db.session.commit()

    token = get_token(client)

    expected = [{"id": 1, "nome": "test"}]

    def fake_init(self, jwt_token=None):
        assert jwt_token == "sessao"
        self.jwt_token = jwt_token

    def fake_envolvidos(self, auto_id):
        assert auto_id == 123
        return expected

    monkeypatch.setattr(AutoPRFClient, "__init__", fake_init)
    monkeypatch.setattr(AutoPRFClient, "get_envolvidos", fake_envolvidos)

    response = client.get(
        "/api/autoprf/envolvidos/123",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.get_json() == expected


def test_autoprf_session_expired(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.autoprf_session = "sessao"
        db.session.commit()
        user_id = user.id

    token = get_token(client)

    def fake_init(self, jwt_token=None):
        assert jwt_token == "sessao"
        self.jwt_token = jwt_token

    def fake_pesquisa(self, numero):
        resp = requests.Response()
        resp.status_code = 401
        raise requests.HTTPError(response=resp)

    monkeypatch.setattr(AutoPRFClient, "__init__", fake_init)
    monkeypatch.setattr(AutoPRFClient, "pesquisa_auto_infracao", fake_pesquisa)

    response = client.post(
        "/api/autoprf/pesquisar_ai",
        json={"auto_infracao": "123"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.get_json() == {"msg": "Sessão AutoPRF expirada"}
    with app.app_context():
        updated = User.query.get(user_id)
        assert updated.autoprf_session is None
