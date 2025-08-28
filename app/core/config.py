from sqlmodel import SQLModel, create_engine, Session
import os

#load_dotenv(dotenv_path="../../.env")

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mysecretpassword@127.0.0.1:5432/tesis_db")

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session 