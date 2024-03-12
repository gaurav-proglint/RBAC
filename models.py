from sqlalchemy import Column,Integer,String
from database import Base

class User(Base):
  __tablename__='User'
  id=Column(Integer,primary_key=True)
  username = Column(String)
  email =Column(String)
  role= Column(String)
  hashed_password =Column(String)

# class Token(Base):
#   __tablename__='Token'
#   access_token: str | None = None
#   refresh_token: str | None = None