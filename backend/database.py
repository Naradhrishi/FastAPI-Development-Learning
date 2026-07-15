from sqlmodel import SQLModel, Session, Field, create_engine

# configure here
DATABASE_URL = "postgresql://postgres:12345678@localhost:5432/mydb"
engine = create_engine(DATABASE_URL, echo = True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
    
def get_session():
    with Session(engine) as session:
        yield session

