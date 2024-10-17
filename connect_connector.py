# add imports
import os
import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes
import pg8000

# Initialize a connection pool for a Cloud SQL instance of Postgres
def connect_with_connector() -> sqlalchemy.engine.base.Engine:
    """Initializes a connection pool for a Cloud SQL instance of Postgres."""
    # Note: Saving credentials in environment variables is convenient, but not
    # secure - consider a more secure solution such as
    # Cloud Secret Manager (https://cloud.google.com/secret-manager) to help
    # keep secrets safe.
    instance_connection_name = os.environ[
        "INSTANCE_CONNECTION_NAME"
    ]  # e.g. 'project:region:instance'
    db_user = os.environ["DB_USER"]  # e.g. 'my-database-user'
    db_pass = os.environ["DB_PASS"]  # e.g. 'my-database-password'
    db_name = os.environ["DB_NAME"]  # e.g. 'my-database'


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
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Create a base class for declarative models
engine = connect_with_connector()
SessionMaker = sessionmaker(bind=engine)
Base = declarative_base()