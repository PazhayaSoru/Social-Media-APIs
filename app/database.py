#from uuid import UUID,uuid4
#import psycopg2
#from psycopg2.extras import RealDictCursor
#import time
#from .database import engine
#from . import models
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings

SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}/{settings.database_name}'

# creates a connection pool to interact with the database.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#
SessionLocal = sessionmaker(autocommit=False,autoflush=False,bind=engine)

#It creates a base class (Base) from which all ORM models should inherit.
Base = declarative_base()

def get_db():
  #A new session (db) is created for interacting with the database.
  db =SessionLocal()
  try:
    #with 'yield' you are creating a single session for each request and using that
    # if you use 'return' instead of 'yield' in the get_db() function, it could lead 
    # to potential issues because the same database session might end up being reused across multiple requests
    yield db
  finally:
    #ensures the session is properly closed after its use,preventing memory leaks
    db.close()



#DB connection variable (Not in Use)
#connect_db = False

#connecting to Database (Not in Use)
#while not connect_db:
#  try:
#    conn = psycopg2.connect(host='localhost',database='fastapi',user='postgres',password='AadhDep@7',cursor_factory=RealDictCursor)
#    cursor = conn.cursor()
#    print("Database connection was successful")
#    connect_db = True
#  except Exception as err:
#    print("Failed to connect to Database")
#    print(f"[ERROR] {err}")
#    time.sleep(2)
