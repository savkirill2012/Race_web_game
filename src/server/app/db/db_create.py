from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base

engine = create_engine('postgresql+psycopg2://test:test@localhost:5432/test')

try:
    engine.connect()
    print(engine)
except:
    print('Error ocure while trying to connect to db')


# Base = declarative_base()

# class Users(Base):
#     __tablename__ = 'users'

#     id = Column(Integer, primary_key=True)
#     username = Column(String(255), unique=True, nullable=False)


# class LeaderBoard(Base):
#     __tablename__ = 'leaderboard'

#     id = Column()