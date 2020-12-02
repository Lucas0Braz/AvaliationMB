from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


url_db = 'sqlite:///data2.db'
engine = create_engine(url_db,
                       connect_args={"check_same_thread": False}
                       )
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base = declarative_base()