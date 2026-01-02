from sqlmodel import SQLModel, create_engine, Session
from typing import Annotated
import os

from dotenv import load_dotenv

load_dotenv(dotenv_path=".env") # defaults to .env if path not specified or just load_dotenv() from python-dotenv

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:mysecretpassword@127.0.0.1:5432/tesis_db")
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]