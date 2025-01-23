from fastapi.testclient import TestClient


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
