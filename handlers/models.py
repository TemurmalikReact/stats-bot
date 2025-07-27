from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, autoincrement=True)        # внутренний
    tg_id = Column(Integer, unique=True)                             # Telegram ID
    ext_id = Column(Integer, unique=True)                            # ваш выдаваемый ID
    first_name = Column(String)
    last_name = Column(String)

class Stat(Base):
    __tablename__ = "stats"
    id = Column(Integer, primary_key=True)
    player_id = Column(Integer, ForeignKey("players.id"))
    goals = Column(Integer, default=0)
    assists = Column(Integer, default=0)
    minutes = Column(Integer, default=0)
