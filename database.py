from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
user="postgres"
password="password"
host="localhost"
port="5432"
database="proglint"

database_url=f'postgresql://{user}:{password}@{host}:{port}/{database}'
engine=create_engine(database_url)
SessionLocal=sessionmaker(autocommit=False,autoflush=False,bind=engine)

Base=declarative_base()

def get_db():
    db=SessionLocal()
    return db


