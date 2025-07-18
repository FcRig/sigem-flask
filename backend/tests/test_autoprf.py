from app.extensions import db
from app.models import User
from app.services.autoprf_client import AutoPRFClient
import requests
import io

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


def test_autoprf_login_strips_whitespace(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        cpf_value = user.cpf

    captured = {}

    def fake_login(self, cpf, password, token):
        captured["cpf"] = cpf
        captured["password"] = password
        captured["token"] = token
        return "jwt-token"

    def fake_init(self, jwt_token=None):
        self.driver = None

    monkeypatch.setattr(AutoPRFClient, "__init__", fake_init)
    monkeypatch.setattr(AutoPRFClient, "login", fake_login)

    token = get_token(client)
    response = client.post(
        "/api/autoprf/login",
        json={"password": " autoprf-pass ", "token": " 123456 "},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert captured == {"cpf": cpf_value, "password": "autoprf-pass", "token": "123456"}

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


def test_pesquisar_ai_strips_whitespace(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.autoprf_session = "sessao"
        db.session.commit()

    token = get_token(client)
    captured = {}

    def fake_init(self, jwt_token=None):
        assert jwt_token == "sessao"
        self.jwt_token = jwt_token

    def fake_pesquisa(self, numero):
        captured["numero"] = numero
        return {}

    monkeypatch.setattr(AutoPRFClient, "__init__", fake_init)
    monkeypatch.setattr(AutoPRFClient, "pesquisa_auto_infracao", fake_pesquisa)

    response = client.post(
        "/api/autoprf/pesquisar_ai",
        json={"auto_infracao": " 1234 "},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert captured.get("numero") == "1234"


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


def test_solicitar_cancelamento_payload(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.autoprf_session = "sessao"
        db.session.commit()

    token = get_token(client)
    captured = {}

    def fake_init(self, jwt_token=None):
        assert jwt_token == "sessao"
        self.jwt_token = jwt_token

    def fake_cancel(self, numero, payload):
        captured["numero"] = numero
        captured["payload"] = payload
        return {"ok": True}

    monkeypatch.setattr(AutoPRFClient, "__init__", fake_init)
    monkeypatch.setattr(AutoPRFClient, "solicitar_cancelamento", fake_cancel)

    list_item = {
        "processo": {"id": 7},
        "tipoSolicitacao": "CANCELAMENTO",
        "justificativa": "just",
        "texto": "motivo",
        "requerente": {"nome": "TEST", "documentos": [{"numero": "123"}]},
    }

    response = client.post(
        "/api/autoprf/solicitacao/cancelamento",
        json={"numero": "123", "list": [list_item]},
        headers={"Authorization": f"Bearer {token}"},
    )

    expected_payload = {"list": [list_item]}

    assert response.status_code == 200
    assert response.get_json() == {"ok": True}
    assert captured == {"numero": "123", "payload": expected_payload}


def test_cancelamento_session_expired(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.autoprf_session = "sessao"
        db.session.commit()
        user_id = user.id

    token = get_token(client)

    def fake_init(self, jwt_token=None):
        assert jwt_token == "sessao"
        self.jwt_token = jwt_token

    def fake_cancel(self, numero, payload):
        resp = requests.Response()
        resp.status_code = 401
        raise requests.HTTPError(response=resp)

    monkeypatch.setattr(AutoPRFClient, "__init__", fake_init)
    monkeypatch.setattr(AutoPRFClient, "solicitar_cancelamento", fake_cancel)

    response = client.post(
        "/api/autoprf/solicitacao/cancelamento",
        json={"numero": "123", "idProcesso": 7},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.get_json() == {"msg": "Sessão AutoPRF expirada"}
    with app.app_context():
        updated = User.query.get(user_id)
        assert updated.autoprf_session is None


def test_historico_returns_data(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.autoprf_session = "sessao"
        db.session.commit()

    token = get_token(client)

    expected = {"status": "ok"}

    def fake_init(self, jwt_token=None):
        assert jwt_token == "sessao"
        self.jwt_token = jwt_token

    def fake_hist(self, pid):
        assert pid == 123
        return expected

    monkeypatch.setattr(AutoPRFClient, "__init__", fake_init)
    monkeypatch.setattr(AutoPRFClient, "historico", fake_hist)

    response = client.get(
        "/api/autoprf/historico/123",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.get_json() == expected


def test_historico_session_expired(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.autoprf_session = "sessao"
        db.session.commit()
        uid = user.id

    token = get_token(client)

    def fake_init(self, jwt_token=None):
        assert jwt_token == "sessao"
        self.jwt_token = jwt_token

    def fake_hist(self, pid):
        resp = requests.Response()
        resp.status_code = 401
        raise requests.HTTPError(response=resp)

    monkeypatch.setattr(AutoPRFClient, "__init__", fake_init)
    monkeypatch.setattr(AutoPRFClient, "historico", fake_hist)

    response = client.get(
        "/api/autoprf/historico/123",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 401
    assert response.get_json() == {"msg": "Sessão AutoPRF expirada"}
    with app.app_context():
        updated = User.query.get(uid)
        assert updated.autoprf_session is None


def test_get_envolvidos_pads_cnpj(monkeypatch):
    expected_id = 77
    raw_data = [{"id": 1, "tipoDocumento": "CNPJ", "numeroDocumento": "1234567890123"}]

    class FakeResponse:
        def __init__(self, data):
            self._data = data
            self.status_code = 200
            self.content = b"1"

        def raise_for_status(self):
            pass

        def json(self):
            return self._data

    def fake_get(url, headers=None):
        assert str(expected_id) in url
        return FakeResponse(raw_data)

    monkeypatch.setattr(requests, "get", fake_get)

    client = AutoPRFClient(jwt_token="token")
    result = client.get_envolvidos(expected_id)

    assert result[0]["numeroDocumento"] == "01234567890123"


def test_anexar_documento_process_route(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.autoprf_session = "sess"
        db.session.commit()

    token = get_token(client)
    captured = {}

    def fake_init(self, jwt_token=None):
        assert jwt_token == "sess"
        self.jwt_token = jwt_token

    def fake_anexar(self, pid, data_bytes, filename):
        captured["pid"] = pid
        captured["bytes"] = data_bytes
        captured["filename"] = filename
        return True

    monkeypatch.setattr(AutoPRFClient, "__init__", fake_init)
    monkeypatch.setattr(AutoPRFClient, "anexar_documento_processo", fake_anexar)

    data = {"file": (io.BytesIO(b"abc"), "doc.pdf")}
    resp = client.post(
        "/api/autoprf/anexar/5",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data=data,
    )

    assert resp.status_code == 200
    assert resp.get_json() == {"ok": True}
    assert captured == {"pid": 5, "bytes": b"abc", "filename": "doc.pdf"}


def test_anexar_documento_session_expired(client, app, monkeypatch):
    with app.app_context():
        user = create_user()
        user.autoprf_session = "sess"
        db.session.commit()
        uid = user.id

    token = get_token(client)

    def fake_init(self, jwt_token=None):
        assert jwt_token == "sess"
        self.jwt_token = jwt_token

    def fake_anexar(self, pid, data_bytes, filename):
        resp = requests.Response()
        resp.status_code = 401
        raise requests.HTTPError(response=resp)

    monkeypatch.setattr(AutoPRFClient, "__init__", fake_init)
    monkeypatch.setattr(AutoPRFClient, "anexar_documento_processo", fake_anexar)

    data = {"file": (io.BytesIO(b"abc"), "doc.pdf")}
    resp = client.post(
        "/api/autoprf/anexar/5",
        headers={"Authorization": f"Bearer {token}"},
        content_type="multipart/form-data",
        data=data,
    )

    assert resp.status_code == 401
    assert resp.get_json() == {"msg": "Sessão AutoPRF expirada"}
    with app.app_context():
        updated = User.query.get(uid)
        assert updated.autoprf_session is None
