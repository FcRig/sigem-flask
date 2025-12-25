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
            "autoprf_session": None,
        }

    token = get_token(client)
    response = client.get(
        "/api/auth/me",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data == expected


def test_register_rejects_duplicate_users(client, app):
    with app.app_context():
        create_user()

    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "password",
            "cpf": "12345678909",
        },
    )

    assert response.status_code == 400
    assert response.get_json() == {"msg": "Usuário já existe"}


def test_update_user_persists_sessions(client, app):
    with app.app_context():
        user = create_user()
        user_id = user.id

    token = get_token(client)

    payload = {
        "autoprf_session": "jwt-session-token",
        "sei_session": "sei-cookie",
        "sei_home_html": "<html>sei</html>",
    }

    response = client.put(
        f"/api/auth/users/{user_id}",
        json=payload,
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == 200

    with app.app_context():
        updated = User.query.get(user_id)
        assert updated.autoprf_session == "jwt-session-token"
        assert updated.sei_session == "sei-cookie"
        assert updated.sei_home_html == "<html>sei</html>"

