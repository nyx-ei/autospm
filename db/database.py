from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

URL_DATABASE = "postgresql://postgres:admin@localhost:5432/autopmDB"

engine = create_engine(URL_DATABASE)

SessionLocal = sessionmaker(autoflush=False, bind=engine)

Base = declarative_base()