from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker


engine = create_engine("sqlite:///hostel.db", echo=True)
Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass


def create_db():
    Base.metadata.create_all(bind=engine)
