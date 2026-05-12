import os
from sqlalchemy import create_engine
from backend.models.engine import Base
from backend.models.database import get_session
from sqlalchemy_utils import drop_database, database_exists
from dotenv import load_dotenv

load_dotenv()
engine = create_engine(os.getenv('URL_DB'))
Base.metadata.drop_all(bind=engine)
