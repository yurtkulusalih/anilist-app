import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from backend.database import get_session
from backend.main import app


@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


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
