from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Bank_transaktioner.models import Base

DATABASE_URL = "postgresql+psycopg2://postgres:Pipi-ina-18@localhost:5432/grupp_arbete_sebank"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)
