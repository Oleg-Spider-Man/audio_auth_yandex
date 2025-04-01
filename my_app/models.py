from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from my_app.database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)
    name = Column(String)
    role = Column(String)

    audio_files = relationship("AudioFile", back_populates="user")


class AudioFile(Base):
    __tablename__ = "audio_files"

    id = Column(Integer, primary_key=True, index=True)
    user_email = Column(String, ForeignKey("users.email"), nullable=False)
    filename = Column(String, nullable=False)
    path = Column(String, nullable=False)

    user = relationship("User", back_populates="audio_files")
