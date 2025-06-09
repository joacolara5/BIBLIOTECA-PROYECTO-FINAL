# base.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Postgres connection: ajusta host/puerto si es necesario
DATABASE_URL = "postgresql+psycopg2://postgres:2deabril2005@localhost:5432/biblioteca"

engine = create_engine(
    DATABASE_URL,
    echo=False,            # True para ver SQL en consola
    future=True
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()
