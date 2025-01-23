from fastapi.testclient import TestClient
from .conftest import create_test_user, authorize_test_user


def test_create_user(client: TestClient):
    mutation = """
        mutation {
            createUser(
                username: "testuser123",
                password: "testpassword")
                }"""

    response = client.post("/graphql", json={"query": mutation})
    data = response.json()

    assert "errors" not in data
    assert data["data"]["createUser"] is True


def test_login(client: TestClient):
    create_test_user(client)

    mutation_login = """
        mutation {
            login(
                username: "testuser123",
                password: "testpassword")
                }"""

    response = client.post("/graphql", json={"query": mutation_login})
    data = response.json()

    assert "errors" not in data
    assert data["data"]["login"] is not None


def test_login_invalid_credentials(client: TestClient):
    create_test_user(client)

    mutation = """
        mutation {
            login(
                username: "testuser123",
                password: "wrongpassword")
                }"""

    response = client.post("/graphql", json={"query": mutation})
    data = response.json()

    assert "errors" in data
    assert data["errors"][0]["message"] == "Invalid credentials"


def test_add_to_watchlist(client: TestClient):
    create_test_user(client)
    auth_data = authorize_test_user(client)

    token = auth_data["data"]["login"]
    mutation = """
        mutation {
            addToWatchlist(
                animeId: 1)
                }"""

    response = client.post(
        "/graphql", json={"query": mutation}, headers={"Authorization": token}
    )
    data = response.json()

    assert "errors" not in data
    assert data["data"]["addToWatchlist"] is True


def test_add_to_watchlist_unauthorized(client: TestClient):
    mutation = """
        mutation {
            addToWatchlist(
                animeId: 1)
                }"""

    response = client.post("/graphql", json={"query": mutation})
    data = response.json()

    assert "errors" in data
    assert data["errors"][0]["message"] == "Unauthorized"


def test_add_to_watchlist_duplicate(client: TestClient):
    create_test_user(client)
    auth_data = authorize_test_user(client)

    token = auth_data["data"]["login"]

    mutation = """
        mutation {
            addToWatchlist(
                animeId: 1)
                }"""

    response = client.post(
        "/graphql", json={"query": mutation}, headers={"Authorization": token}
    )
    data = response.json()

    assert "errors" not in data
    assert data["data"]["addToWatchlist"] is True

    response = client.post(
        "/graphql", json={"query": mutation}, headers={"Authorization": token}
    )
    data = response.json()

    assert "errors" in data
    assert data["errors"][0]["message"] == "Anime already in the watchlist"
