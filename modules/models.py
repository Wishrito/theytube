from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from modules.database import Base

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    discord_id = Column(Integer, unique=True, nullable=False)

    def __repr__(self):
        return f"<User(discord_id='{self.discord_id}')>"


class UserHistory(Base):
    __tablename__ = "user_history"
    id = Column(Integer, primary_key=True, autoincrement=True, )
    user_id = Column(Integer, nullable=False)
    video_id = Column(String, nullable=False)

    def __repr__(self):
        return f"<UserHistory(user_id='{self.user_id}', video_id='{self.video_id}')>"
