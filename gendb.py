from app import app
from app.views import genId
from sqlalchemy import create_engine
from sqlalchemy.sql import text
import pandas as pd
from faker import Faker
from sqlalchemy.orm import scoped_session, sessionmaker
from collections import defaultdict
import time

# Sets up connections to database using database settings stored in environment variable
conn = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])

start = time.time()
#Generates Tables from sql file
with conn.connect() as con:
    file = open('app/static/SQL/meal_system.sql')
    query = text(file.read())
    con.execute(query)
    #con.close()
end = time.time()
lap = end - start
print("successfully populated database in ",lap, "seconds")

