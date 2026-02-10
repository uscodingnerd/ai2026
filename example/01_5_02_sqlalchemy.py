from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine("sqlite:///example.db")
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)

# Create table(s)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

user = User(name="Alice", email="alice@example.com")
session.add(user)
session.commit()

for u in session.query(User):
    print(u.name, u.email)
