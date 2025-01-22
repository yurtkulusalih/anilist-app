from sqlmodel import Field, Relationship, SQLModel


class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    username: str = Field(unique=True)
    password: str

    watchlist_items: list["Watchlist"] = Relationship(back_populates="user")


class Watchlist(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    anime_id: int

    user_id: int = Field(foreign_key="user.id")
    user: User | None = Relationship(back_populates="watchlist_items")
