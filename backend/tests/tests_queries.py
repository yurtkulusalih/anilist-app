from fastapi.testclient import TestClient
from .conftest import create_test_user, authorize_test_user


def populate_watchlist(client: TestClient, token):
    mutation = """
        mutation {
            addToWatchlist(
                animeId: 1)
                }"""

    client.post("/graphql", json={"query": mutation}, headers={"Authorization": token})


def test_search_anime(client: TestClient):
    query = """
        query{
            animelist(search: "Naruto") {
                id
                title
                description
                averageScore
                coverImage
                startDate
                endDate
                status
            }
        }
    """
    response = client.post("/graphql", json={"query": query})
    data = response.json()

    assert "errors" not in data
    assert data["data"] is not None
    assert len(data["data"]["animelist"]) > 0


def test_get_watchlist(client: TestClient):
    create_test_user(client)
    auth_data = authorize_test_user(client)
    token = auth_data["data"]["login"]

    populate_watchlist(client, token)

    query = """
        query{
            getWatchlist {
                id
            }
        }
    """
    response = client.post(
        "/graphql", json={"query": query}, headers={"Authorization": token}
    )
    data = response.json()

    assert "errors" not in data
    assert data["data"] is not None
    assert len(data["data"]["getWatchlist"]) > 0
    assert data["data"]["getWatchlist"][0]["id"] == 1


def test_get_watchlist_unauthorized(client: TestClient):
    create_test_user(client)
    auth_data = authorize_test_user(client)
    token = auth_data["data"]["login"]

    populate_watchlist(client, token)

    query = """
        query{
            getWatchlist {
                id
            }
        }
    """
    # It seems a bit weird since we already have to authorize the user to populate the watchlist
    response = client.post("/graphql", json={"query": query})
    data = response.json()

    assert "errors" in data
    assert data["errors"][0]["message"] == "Unauthorized"
