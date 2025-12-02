from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./vida_plus.db"  # depois você pode trocar para PostgreSQL

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}  # necessário para SQLite no modo single-thread
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
