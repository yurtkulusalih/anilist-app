import pytest
from sqlmodel import Session, SQLModel, create_engine
from fastapi.testclient import TestClient
from sqlmodel.pool import StaticPool

from backend.database import get_session

from backend.main import app


# Works like a fixture
def create_test_user(client: TestClient):
    mutation_create_user = """
        mutation {
            createUser(
                username: "testuser123",
                password: "testpassword")
                }"""

    client.post("/graphql", json={"query": mutation_create_user})


def authorize_test_user(client: TestClient):
    mutation_login = """
        mutation {
            login(
                username: "testuser123",
                password: "testpassword")
                }"""

    response = client.post("/graphql", json={"query": mutation_login})
    return response.json()


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
