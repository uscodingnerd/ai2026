from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String

engine = create_engine("sqlite:///example2.db")
metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String),
    Column('email', String)
)

metadata.create_all(engine)

# Insert data
with engine.connect() as conn:
    conn.execute(
        users.insert().values(
            name="Bob",
            email="bob@example.com"
        )
    )
