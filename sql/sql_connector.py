import os
from google.cloud.sql.connector import Connector, IPTypes
import sqlalchemy

import pg8000
from sqlalchemy.ext.declarative import declarative_base

# Initialize a connection pool for a Cloud SQL instance of Postgres
def cloudsql_connector() -> sqlalchemy.engine.base.Engine:
   # Initializes a connection pool for a Cloud SQL instance of Postgres
   instance_connection_name = os.environ["INSTANCE_CONNECTION_NAME"]  # e.g. 'project:region:instance'
   db_user = os.environ["DB_USER"]
   db_pass = os.environ["DB_PASS"]
   db_name = os.environ["DB_NAME"]
   ip_type = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC
   connector = Connector()

   def getconn() -> sqlalchemy.engine.base.Engine:
       conn: sqlalchemy.engine.base.Engine = connector.connect(
           instance_connection_name,
           "pg8000",
           user=db_user,
           password=db_pass,
           db=db_name,
           ip_type=ip_type,
       )
       return conn

   pool = sqlalchemy.create_engine(
       "postgresql+pg8000://",
       creator=getconn,
       # ...
   )
   return pool

# Create a connection pool
engine = cloudsql_connector()
# Create a sessionmaker class to create new sessions
SessionMaker = sqlalchemy.orm.sessionmaker(bind=engine)
# Create a Base class for ORM
Base = declarative_base()