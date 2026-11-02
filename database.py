import os
from dotenv import load_dotenv
from sqlalchemy import URL
from sqlmodel import Session, create_engine

load_dotenv()

if os.getenv("POSTGRES_HOST"):
    database_url = URL.create(
        drivername="postgresql+psycopg",
        username=os.environ["POSTGRES_USER"],
        password=os.environ["POSTGRES_PASSWORD"],
        host=os.environ["POSTGRES_HOST"],
        port=5432,
        database=os.environ["POSTGRES_DB"]
    )
else:
    database_url = os.environ["DATABASE_URL"]

engine = create_engine(database_url)

def get_session():
    with Session(engine) as session:
        yield session