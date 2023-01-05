# __init__.py = turns folder into a package
from os import getenv
from sqlalchemy.ext.declarative import declarative_base # Used to create classes
from sqlalchemy import create_engine # Engines are used to interpret data from the database
from sqlalchemy.orm import sessionmaker # Sessions used to maintain connection to database
from dotenv import load_dotenv

load_dotenv() # Load environment

# Connect to db
engine = create_engine(getenv('DB_URL'), echo = True, pool_size = 20, max_overflow = 0) 
# echo = True -> creates logs of data inputs
# pool_size = 20 -> declares number of connections open in connection pool. 0 for no limit, default 5
# max_overflow = 0 -> declares number of possible overflow connections in connection pool, only used in QueuePool
Session = sessionmaker(bind=engine) # -> binds session to the specific engine
Base = declarative_base() 

