from contextvars import ContextVar
from sqlmodel import create_engine, SQLModel, Session
from config import DATABASE_URL


def get_session():
    engine = create_engine(DATABASE_URL, echo=True)
    with Session(engine) as session:
        yield session

