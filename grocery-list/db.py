from sqlalchemy import create_engine

DATABASE_URL = "postgresql://postgres:april0415@localhost:5432/grocery_list"

engine = create_engine(DATABASE_URL, echo=True)