from sqlalchemy import Column, Integer, String

from my_app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    name = Column(String)
    role = Column(String)
