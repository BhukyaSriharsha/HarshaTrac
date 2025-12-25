from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from urllib.parse import quote_plus

password = quote_plus("Sriharsha@131718")
db_url = f"postgresql://postgres:{password}@localhost:5432/harsha"
engine = create_engine(db_url)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)