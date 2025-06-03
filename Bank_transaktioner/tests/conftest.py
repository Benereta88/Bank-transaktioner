import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from Bank_transaktioner.models import Base  # byt ut mot din verkliga modulsökväg

DATABASE_URL = "postgresql://postgres:Pipi-ina-18@localhost/grupp_arbete_sebank"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

@pytest.fixture
def db_session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    session = Session()
    try:
        yield session
    finally:
        session.close()