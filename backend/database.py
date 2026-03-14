from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///answercheck.db"

engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables() -> None:
    SQLModel.metadata.create_all(engine)
