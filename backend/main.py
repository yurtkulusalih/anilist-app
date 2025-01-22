from contextlib import asynccontextmanager
from fastapi import FastAPI
from strawberry.fastapi import GraphQLRouter
from .database import create_db_and_tables
from .schema import schema


@asynccontextmanager
async def setup_db(app: FastAPI):
    create_db_and_tables()
    yield


graphql_app = GraphQLRouter(schema=schema)

app = FastAPI(lifespan=setup_db)

app.include_router(graphql_app, prefix="/graphql")
