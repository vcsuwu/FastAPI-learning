import os
from typing import Annotated
import urllib.parse
from sqlmodel import Field, SQLModel, create_engine, Session, select
from fastapi import Depends, FastAPI

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]

class Product(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    price: int

DB_USER = os.getenv("DB_USER", "hollow")
DB_NAME = os.getenv("PGDATABASE", "default")
DB_HOST = os.getenv("PGHOST", "")

encoded_path = urllib.parse.quote_plus(DB_HOST)
database_url = f"postgresql+psycopg://{DB_USER}@/{DB_NAME}?host={encoded_path}"
engine = create_engine(database_url, echo=True)

def create_db_and_tables():  
    SQLModel.metadata.create_all(engine)  

def create_products():
    product_1 = Product(name="Pivo", price=1000)
    product_2 = Product(name="Kvas", price=1000)
    product_3 = Product(name="Prikol", price=1000)
    with Session(engine) as session:
        session.add(product_1)
        session.add(product_2)
        session.add(product_3)
        session.commit()

def main():
    create_db_and_tables()
    create_products()

if __name__ == "__main__":  
    main()


app = FastAPI()

@app.get('/products')
def products(session: SessionDep):
    products = session.exec(select(Product)).all()
    return products




