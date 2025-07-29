from app.models import User
from app.extensions import db
from app.services.sei_client import SEIClient
import requests
import json
from unittest.mock import MagicMock


def create_user():
    user = User(
        username="testuser",
        email="test@example.com",
        administrador=False,
        cpf="12345678909",
    )
    user.set_password("password")
    user.usuario_sei = "seiuser"
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
        self.session = requests.Session()

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


def test_sei_login_stores_session(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user_id = user.id

    def fake_init(self, session=None):
        self.session = requests.Session()

    def fake_login(self, usuario, senha, tok):
        self.session.cookies.set("SID", "ABC")

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(SEIClient, "login", fake_login)

    token = get_token(client)
    resp = client.post(
        "/api/sei/login",
        json={"usuario": "seiuser", "senha_sei": "pass", "token_sei": "1"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 200
    with app.app_context():
        updated = User.query.get(user_id)
        assert json.loads(updated.sei_session)["SID"] == "ABC"


def test_sei_login_strips_whitespace(client, app, monkeypatch):
    with app.app_context():
        create_user()
    token = get_token(client)

    captured = {}

    def fake_init(self, session=None):
        self.session = requests.Session()

    def fake_login(self, usuario, senha, tok):
        captured["u"] = usuario
        captured["s"] = senha
        captured["t"] = tok

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(SEIClient, "login", fake_login)

    response = client.post(
        "/api/sei/login",
        json={"usuario": " seiuser ", "senha_sei": " senha ", "token_sei": " 123 "},
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


def test_list_process_types_calls_client(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.sei_session = json.dumps({"SID": "ABC"})
        db.session.commit()
    token = get_token(client)

    captured = {}

    def fake_init(self, session=None):
        captured["cookie"] = session.cookies.get("SID")

    def fake_list(self):
        return [{"id": "1", "text": "Proc"}]

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(SEIClient, "list_process_types", fake_list)

    response = client.post(
        "/api/sei/tipos",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.get_json() == [{"id": "1", "text": "Proc"}]
    assert captured == {"cookie": "ABC"}


def test_create_process_calls_client(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.sei_session = json.dumps({"SID": "ABC"})
        db.session.commit()
    token = get_token(client)

    captured = {}

    def fake_init(self, session=None):
        captured["cookie"] = session.cookies.get("SID")

    def fake_create(self, tipo_id, tipo_nome, desc):
        captured["id"] = tipo_id
        captured["nome"] = tipo_nome
        captured["desc"] = desc
        resp = requests.Response()
        resp.status_code = 200
        return resp

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(SEIClient, "create_process", fake_create)

    payload = {
        "tipo_id": "7",
        "tipo_nome": "Teste",
        "descricao": "desc",
    }
    response = client.post(
        "/api/sei/processos",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.get_json() == {"msg": "Processo criado com sucesso"}
    assert captured == {"cookie": "ABC", "id": "7", "nome": "Teste", "desc": "desc"}


def test_tipos_invokes_login_and_list(client, app, monkeypatch):
    """Ensure list endpoint calls SEIClient methods."""
    with app.app_context():
        user = create_user()
        user.sei_session = json.dumps({"SID": "AB"})
        db.session.commit()
    token = get_token(client)

    def fake_init(self, session=None):
        pass

    list_mock = MagicMock(return_value=[{"id": "1", "text": "Proc"}])

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(SEIClient, "list_process_types", list_mock)

    resp = client.post(
        "/api/sei/tipos",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 200
    list_mock.assert_called_once_with()


def test_processos_invokes_login_and_create(client, app, monkeypatch):
    """Ensure process creation endpoint calls SEIClient methods with args."""
    with app.app_context():
        user = create_user()
        user.sei_session = json.dumps({"SID": "AB"})
        db.session.commit()
    token = get_token(client)

    def fake_init(self, session=None):
        pass

    resp_obj = requests.Response()
    resp_obj.status_code = 200
    create_mock = MagicMock(return_value=resp_obj)

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(SEIClient, "create_process", create_mock)

    payload = {
        "tipo_id": "7",
        "tipo_nome": "Teste",
        "descricao": "desc",
    }
    resp = client.post(
        "/api/sei/processos",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 200
    create_mock.assert_called_once_with("7", "Teste", "desc")


def test_sei_session_expired(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.sei_session = json.dumps({"SID": "AB"})
        db.session.commit()
        uid = user.id

    token = get_token(client)

    def fake_init(self, session=None):
        pass

    def fake_list(self):
        resp = requests.Response()
        resp.status_code = 401
        raise requests.HTTPError(response=resp)

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(SEIClient, "list_process_types", fake_list)

    resp = client.post(
        "/api/sei/tipos",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 401
    assert resp.get_json() == {"msg": "Sessão SEI expirada"}
    with app.app_context():
        updated = User.query.get(uid)
        assert updated.sei_session is None
