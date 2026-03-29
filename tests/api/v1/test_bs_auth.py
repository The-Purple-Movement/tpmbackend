import pytest
from app.core.deps import get_current_user
from app.repositories.bs_user_repo import get_user_by_email

# Prefix for all endpoints in this module
PREFIX = "/api/v1/bs"

def test_register_success(client):
    response = client.post(
        f"{PREFIX}/register",
        json={
            "email": "newuser@example.com",
            "password": "Password123!",
            "full_name": "New User"
        }
    )
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_register_invalid_email(client):
    response = client.post(
        f"{PREFIX}/register",
        json={
            "email": "not-an-email",
            "password": "Password123!",
            "full_name": "New User"
        }
    )
    assert response.status_code == 422 # Pydantic validation error

def test_login_success(client, db):
    # Register first
    client.post(
        f"{PREFIX}/register",
        json={
            "email": "loginuser@example.com",
            "password": "Password123!",
            "full_name": "Login User"
        }
    )
    
    response = client.post(
        f"{PREFIX}/login",
        json={
            "email": "loginuser@example.com",
            "password": "Password123!"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data

def test_login_wrong_password(client, db):
    client.post(
        f"{PREFIX}/register",
        json={
            "email": "wrongpwd@example.com",
            "password": "Password123!",
            "full_name": "User"
        }
    )
    
    response = client.post(
        f"{PREFIX}/login",
        json={
            "email": "wrongpwd@example.com",
            "password": "WrongPassword123"
        }
    )
    # The status code depends on implementation, likely 401 or 404
    assert response.status_code in [401, 404]

def test_refresh_token_success(client, db):
    # Register and get refresh token
    reg_resp = client.post(
        f"{PREFIX}/register",
        json={
            "email": "refresh@example.com",
            "password": "Password123!",
            "full_name": "Refresh User"
        }
    )
    refresh_token = reg_resp.json()["refresh_token"]
    
    response = client.post(
        f"{PREFIX}/refresh",
        json={"refresh_token": refresh_token}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data

def test_get_me_success(client, mock_user, db):
    # Use real user in DB for repository mocks if necessary
    db.add(mock_user)
    db.commit()
    db.refresh(mock_user)
    
    # Override authentication
    from app.main import app
    app.dependency_overrides[get_current_user] = lambda: mock_user
    
    response = client.get(f"{PREFIX}/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == mock_user.email
    assert data["full_name"] == mock_user.full_name
    
    app.dependency_overrides.pop(get_current_user, None)

def test_update_me_success(client, db):
    # Register a real user
    client.post(
        f"{PREFIX}/register",
        json={
            "email": "update@example.com",
            "password": "Password123!",
            "full_name": "Original Name"
        }
    )
    
    user = get_user_by_email(db, "update@example.com")
    
    from app.main import app
    app.dependency_overrides[get_current_user] = lambda: user
    
    response = client.put(
        f"{PREFIX}/me",
        json={"full_name": "Updated Name"}
    )
    assert response.status_code == 200
    assert response.json()["full_name"] == "Updated Name"
    
    # Verify in DB
    db.refresh(user)
    assert user.full_name == "Updated Name"
    
    app.dependency_overrides.pop(get_current_user, None)

def test_change_password_success(client, db):
    client.post(
        f"{PREFIX}/register",
        json={
            "email": "changepwd@example.com",
            "password": "OldPassword123!",
            "full_name": "Pwd User"
        }
    )
    
    user = get_user_by_email(db, "changepwd@example.com")
    
    from app.main import app
    app.dependency_overrides[get_current_user] = lambda: user
    
    response = client.post(
        f"{PREFIX}/change-password",
        json={
            "current_password": "OldPassword123!",
            "new_password": "NewPassword123!"
        }
    )
    assert response.status_code == 200
    
    # Verify login with new password
    app.dependency_overrides.pop(get_current_user, None)
    login_resp = client.post(
        f"{PREFIX}/login",
        json={
            "email": "changepwd@example.com",
            "password": "NewPassword123!"
        }
    )
    assert login_resp.status_code == 200
