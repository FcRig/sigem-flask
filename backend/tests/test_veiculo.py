from app.extensions import db
from app.models import User
from app.services.veiculo_client import VeiculoClient


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


def test_consultar_placa_returns_data(client, app, monkeypatch):
    with app.app_context():
        create_user()

    token = get_token(client)

    expected = {"placa": "ABC1234", "marca": "TEST"}

    def fake_consultar(self, placa):
        assert placa == "ABC1234"
        return expected

    monkeypatch.setattr(VeiculoClient, "consultar_placa", fake_consultar)

    response = client.post(
        "/api/veiculo/placa",
        json={"placa": "ABC1234"},
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200
    assert response.get_json() == expected


def test_consultar_placa_requires_jwt(client, app, monkeypatch):
    with app.app_context():
        create_user()

    # No token provided
    response = client.post(
        "/api/veiculo/placa",
        json={"placa": "XYZ9999"},
    )

    assert response.status_code == 401
