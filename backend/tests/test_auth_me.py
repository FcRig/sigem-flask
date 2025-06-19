from app.extensions import db
from app.models import User


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


def test_me_returns_user_details(client, app):
    with app.app_context():
        user = create_user()
        expected = {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "administrador": user.administrador,
            "cpf": user.cpf,
        }

    token = get_token(client)
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data == expected

