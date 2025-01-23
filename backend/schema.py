from typing import List
from sqlmodel import Session, select
import requests
import bcrypt
import jwt
import strawberry
from strawberry.types import Info
from .models import User, Watchlist

SECRET_KEY = "a07ebd8f4351b053da2ad3713db479b0c33444d2ca741f47a1eee6eff2d0844f"

search_anime_query = """
        query ($page: Int = 1, $type: MediaType = ANIME, $search: String, $status: MediaStatus ) {
            Page (page: $page, perPage: 50) {
                pageInfo {
                    total
                    currentPage
                    hasNextPage
                    perPage
                }
                media (search: $search, type: $type, status: $status) {
                    id
                    title {
                        userPreferred
                    }
                    description
                    averageScore
                    coverImage {
                        large
                    }
                    startDate {
                        day
                        month
                        year
                    }
                    endDate {
                        day
                        month
                        year
                    }
                    status(version: 2)
                }
            }
        }
        """

fetch_media_list = """
        query ($ids: [Int]) {
            Page {
                media (id_in: $ids, type: ANIME) {
                    id
                    title {
                        userPreferred
                    }
                    averageScore
                    coverImage {
                        large
                    }
                    startDate {
                        day
                        month
                        year
                    }
                    endDate {
                        day
                        month
                        year
                    }
                    status(version: 2)
                }
            }
        }
        """


@strawberry.type
class AnimeBaseType:
    id: int
    title: str
    coverImage: str | None
    averageScore: float | None
    startDate: str | None
    endDate: str | None
    status: str


@strawberry.type
class AnimeType(AnimeBaseType):
    description: str | None


@strawberry.type
class WatchlistItemType:
    id: int
    anime_id: int


@strawberry.type
class UserWatchlistType(AnimeBaseType):
    pass


def verify_auhorization(headers):
    token = headers.get("Authorization")
    if not token:
        raise Exception("Unauthorized")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload["username"]
        return username
    except jwt.InvalidTokenError:
        raise Exception("Invalid token")


@strawberry.type
class Query:
    # Page size is fixed to 20
    # TODO: could be improved by adding pagination
    @strawberry.field
    def animelist(self, search: str) -> List[AnimeType]:
        variables = None if search == "" else {"search": search}
        response = requests.post(
            "https://graphql.anilist.co",
            json={"query": search_anime_query, "variables": variables},
        )
        data = response.json()

        return [
            AnimeType(
                id=anime["id"],
                title=anime["title"]["userPreferred"],
                description=anime["description"],
                averageScore=anime["averageScore"],
                coverImage=anime["coverImage"]["large"],
                startDate=f"{anime['startDate']['day']}-{anime['startDate']['month']}-{anime['startDate']['year']}",
                endDate=f"{anime['endDate']['day']}-{anime['endDate']['month']}-{anime['endDate']['year']}",
                status=anime["status"],
            )
            for anime in data["data"]["Page"]["media"]
        ]

    @strawberry.field
    def get_watchlist(self, info: Info) -> List[UserWatchlistType]:
        session = info.context["session"]
        request = info.context["request"]
        try:
            username = verify_auhorization(request.headers)
            user = session.exec(select(User).where(User.username == username)).first()

            watchlist = session.exec(
                select(Watchlist).where(Watchlist.user_id == user.id)
            )

            anime_ids = [item.anime_id for item in watchlist]
            variables = {"ids": anime_ids}
            response = requests.post(
                "https://graphql.anilist.co",
                json={"query": fetch_media_list, "variables": variables},
            )
            data = response.json()

            return [
                UserWatchlistType(
                    id=anime["id"],
                    title=anime["title"]["userPreferred"],
                    coverImage=anime["coverImage"]["large"],
                    averageScore=anime["averageScore"],
                    startDate=f"{anime['startDate']['day']}-{anime['startDate']['month']}-{anime['startDate']['year']}",
                    endDate=f"{anime['endDate']['day']}-{anime['endDate']['month']}-{anime['endDate']['year']}",
                    status=anime["status"],
                )
                for anime in data["data"]["Page"]["media"]
            ]
        except Exception as e:
            raise e


@strawberry.type
class Mutation:
    @strawberry.mutation
    def create_user(self, username: str, password: str, info: Info) -> bool:
        # Leverage dependency injection to get the session
        session: Session = info.context["session"]
        hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        user = User(username=username, password=hashed_password.decode("utf-8"))
        session.add(user)
        session.commit()

        return True

    @strawberry.mutation
    def login(self, username: str, password: str, info: Info) -> str:
        session: Session = info.context["session"]
        user = session.exec(select(User).where(User.username == username)).first()
        if not user or not bcrypt.checkpw(
            password.encode("utf-8"), user.password.encode("utf-8")
        ):
            raise Exception("Invalid credentials")

        token = jwt.encode({"username": username}, SECRET_KEY, algorithm="HS256")
        return token

    @strawberry.mutation
    def add_to_watchlist(self, anime_id: int, info: Info) -> bool:
        session: Session = info.context["session"]
        request = info.context["request"]
        try:
            username = verify_auhorization(request.headers)
            user = session.exec(select(User).where(User.username == username)).first()

            if session.exec(
                select(Watchlist).where(
                    Watchlist.anime_id == anime_id, Watchlist.user_id == user.id
                )
            ).first():
                raise Exception("Anime already in the watchlist")

            watchlist = Watchlist(anime_id=anime_id, user_id=user.id)
            session.add(watchlist)
            session.commit()
            return True
        except Exception as e:
            raise e


schema = strawberry.Schema(query=Query, mutation=Mutation)
