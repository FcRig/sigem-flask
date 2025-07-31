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
        self.home_html = None

    def fake_login(self, usuario, senha, tok):
        captured["u"] = usuario
        captured["s"] = senha
        captured["t"] = tok
        self.home_html = "<html>home</html>"

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
        self.home_html = "<html>home</html>"

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
        assert updated.sei_home_html == "<html>home</html>"


def test_sei_login_strips_whitespace(client, app, monkeypatch):
    with app.app_context():
        create_user()
    token = get_token(client)

    captured = {}

    def fake_init(self, session=None):
        self.session = requests.Session()
        self.home_html = None

    def fake_login(self, usuario, senha, tok):
        captured["u"] = usuario
        captured["s"] = senha
        captured["t"] = tok
        self.home_html = "<html>home</html>"

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
        user.sei_home_html = "<html>home</html>"
        db.session.commit()
    token = get_token(client)

    captured = {}

    def fake_init(self, session=None):
        captured["cookie"] = session.cookies.get("SID")

    def fake_list(self):
        captured["html"] = self.home_html
        return [{"id": "1", "text": "Proc"}]

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(SEIClient, "list_process_types", fake_list)

    response = client.post(
        "/api/sei/tipos",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.get_json() == [{"id": "1", "text": "Proc"}]
    assert captured == {"cookie": "ABC", "html": "<html>home</html>"}


def test_create_process_calls_client(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.sei_session = json.dumps({"SID": "ABC"})
        user.sei_home_html = "<html>home</html>"
        db.session.commit()
    token = get_token(client)

    captured = {}

    def fake_init(self, session=None):
        captured["cookie"] = session.cookies.get("SID")

    def fake_create(self, tipo_id, tipo_nome, desc):
        captured["id"] = tipo_id
        captured["nome"] = tipo_nome
        captured["desc"] = desc
        captured["html"] = self.home_html
        resp = requests.Response()
        resp.status_code = 200
        return resp

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(SEIClient, "create_process", fake_create)
    monkeypatch.setattr(SEIClient, "get_current_unit", lambda self: "X")
    monkeypatch.setattr(SEIClient, "change_unit", lambda self, u: None)

    payload = {
        "tipo_id": "7",
        "tipo_nome": "Teste",
        "descricao": "desc",
        "unidade": "X",
    }
    response = client.post(
        "/api/sei/processos",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.get_json() == {"msg": "Processo criado com sucesso"}
    assert captured == {
        "cookie": "ABC",
        "id": "7",
        "nome": "Teste",
        "desc": "desc",
        "html": "<html>home</html>",
    }


def test_tipos_invokes_login_and_list(client, app, monkeypatch):
    """Ensure list endpoint calls SEIClient methods."""
    with app.app_context():
        user = create_user()
        user.sei_session = json.dumps({"SID": "AB"})
        user.sei_home_html = "<html>home</html>"
        db.session.commit()
    token = get_token(client)

    def fake_init(self, session=None):
        self.home_html = None

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
        user.sei_home_html = "<html>home</html>"
        db.session.commit()
    token = get_token(client)

    def fake_init(self, session=None):
        self.home_html = None

    resp_obj = requests.Response()
    resp_obj.status_code = 200
    create_mock = MagicMock(return_value=resp_obj)

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(SEIClient, "create_process", create_mock)
    monkeypatch.setattr(SEIClient, "get_current_unit", lambda self: "X")
    monkeypatch.setattr(SEIClient, "change_unit", lambda self, u: None)

    payload = {
        "tipo_id": "7",
        "tipo_nome": "Teste",
        "descricao": "desc",
        "unidade": "X",
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
        user.sei_home_html = "<html>home</html>"
        db.session.commit()
        uid = user.id

    token = get_token(client)

    def fake_init(self, session=None):
        self.home_html = None

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
        assert updated.sei_home_html is None


class DummyResp:
    def __init__(self, text=""):
        self.text = text
        self.encoding = "iso-8859-1"


def _setup_create_mocks(monkeypatch, session, captured):
    def fake_link_action(self, html, action):
        return "a"

    def fake_link_text(self, html, text):
        return "b"

    call = {"n": 0}

    def fake_get(url):
        call["n"] += 1
        if call["n"] == 1:
            return DummyResp()
        return DummyResp('<form id="frmProcedimentoCadastro" action="c"></form>')

    def fake_post(url, data=None):
        captured["data"] = data
        captured["url"] = url
        return DummyResp()

    session.get = fake_get
    session.post = fake_post
    monkeypatch.setattr(SEIClient, "get_link_by_action", fake_link_action)
    monkeypatch.setattr(SEIClient, "get_link_by_text", fake_link_text)


def test_create_process_sets_assunto_cancelamento(monkeypatch):
    session = requests.Session()
    client = SEIClient(session=session)
    client.home_html = "<html></html>"
    captured = {}
    _setup_create_mocks(monkeypatch, session, captured)

    client.create_process("1", "Multas: Auto de Infração - Cancelamento", "d")

    assert captured["data"]["hdnAssuntos"] == "727"


def test_create_process_sets_assunto_default(monkeypatch):
    session = requests.Session()
    client = SEIClient(session=session)
    client.home_html = "<html></html>"
    captured = {}
    _setup_create_mocks(monkeypatch, session, captured)

    client.create_process("1", "Outro Processo", "d")

    assert captured["data"]["hdnAssuntos"] == "209"


def test_list_units_calls_client(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.sei_session = json.dumps({"SID": "ABC"})
        user.sei_home_html = "<html>home</html>"
        db.session.commit()
    token = get_token(client)

    def fake_init(self, session=None):
        assert session.cookies.get("SID") == "ABC"
        self.home_html = None

    list_mock = MagicMock(return_value=[{"id": "1", "text": "U"}])

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(SEIClient, "list_units", list_mock)

    resp = client.post(
        "/api/sei/unidades",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 200
    list_mock.assert_called_once_with()


def test_criar_processo_changes_unit_when_different(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.sei_session = json.dumps({"SID": "AB"})
        user.sei_home_html = "<a id='lnkInfraUnidade'>A</a>"
        db.session.commit()
    token = get_token(client)

    def fake_init(self, session=None):
        self.home_html = "<a id='lnkInfraUnidade'>A</a>"

    create_resp = requests.Response()
    create_resp.status_code = 200

    monkeypatch.setattr(SEIClient, "__init__", fake_init)
    monkeypatch.setattr(
        SEIClient, "create_process", MagicMock(return_value=create_resp)
    )
    change_mock = MagicMock()
    monkeypatch.setattr(SEIClient, "change_unit", change_mock)
    monkeypatch.setattr(SEIClient, "get_current_unit", lambda self: "A")

    payload = {
        "tipo_id": "1",
        "tipo_nome": "T",
        "descricao": "d",
        "unidade": "B",
    }

    resp = client.post(
        "/api/sei/processos",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert resp.status_code == 200
    change_mock.assert_called_once_with("B")
