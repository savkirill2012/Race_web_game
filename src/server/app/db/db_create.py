from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, Session

engine = create_engine('postgresql+psycopg2://test:test@localhost:5432/test', echo=True)

try:
    engine.connect()
    print(engine)
except:
    print('Error ocure while trying to connect to db')


Base = declarative_base()

class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    # leaderboard = relationship('LeaderBoard', uselist=False)

    def __repr__(self) -> str:
        return f'{self.id} {self.username}'


# class LeaderBoard(Base):
#     __tablename__ = 'leaderboard'

#     id = Column(Integer, primary_key=True)
#     username = Column(String(255), ForeignKey('leaderboard.username'), unique=True, nullable=False)
#     score = Column(Integer)

#     def __repr__(self) -> str:
#         return f'{self.id} {self.username} {self.score}'

if __name__ == '__main__':
    Base.metadata.create_all(engine)
    with Session(autoflush=False, bind=engine) as db:
        # new_user = Users(username='Test5')
        # db.add(new_user)
        # db.commit()
        res = db.query(Users).all()
        print(res)

