from typing import List
import requests
import strawberry

search_anime_query = """
        query ($page: Int = 1, $type: MediaType = ANIME, $search: String, $status: MediaStatus ) {
            Page (page: $page, perPage: 20) {
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


@strawberry.type
class AnimeType:
    id: int
    title: str
    description: str
    averageScore: float | None
    coverImage: str  # URL
    startDate: str | None
    endDate: str | None
    status: str


@strawberry.type
class WatchlistItemType:
    id: int
    anime_id: int


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


schema = strawberry.Schema(query=Query)
