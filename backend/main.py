from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter
from .database import create_db_and_tables, get_session
from .schema import schema


@asynccontextmanager
async def setup_db(app: FastAPI):
    create_db_and_tables()
    yield


def get_context(session=Depends(get_session)):
    return {"session": session}


graphql_app = GraphQLRouter(schema=schema, context_getter=get_context)

app = FastAPI(lifespan=setup_db)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(graphql_app, prefix="/graphql")
