from fastapi import FastAPI
from .database.core import Base, engine
from .entities.todo import Todo
from .entities.user import User
from .api import register_routes
from .logging import configure_logging, LogLevels
import logging
configure_logging(LogLevels.info)

# Create all tables
Base.metadata.create_all(bind=engine)
logging.info("Tables created")

app = FastAPI()
register_routes(app)