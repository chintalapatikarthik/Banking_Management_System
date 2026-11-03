import pytest
import os
import sys

# Ensure project root is in path and configure isolated SQLite test DB BEFORE importing app modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ['DATABASE_URL'] = 'sqlite:///test_suite.db'

from sqlalchemy import create_engine
import app.database
test_engine = create_engine('sqlite:///test_suite.db')
app.database.engine = test_engine
app.database.SessionLocal.configure(bind=test_engine)

from app import create_app
from app.config import Config
from app.database import Base, get_db
from database.init_db import init_database

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_suite.db'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key-1234'

@pytest.fixture(scope='session')
def app():
    app = create_app(TestConfig)
    return app

@pytest.fixture(scope='function')
def client(app):
    return app.test_client()

@pytest.fixture(scope='function')
def runner(app):
    return app.test_cli_runner()

@pytest.fixture(scope='session', autouse=True)
def clean_database_after_all_tests():
    yield
    try:
        if os.path.exists('test_suite.db'):
            os.remove('test_suite.db')
    except Exception as e:
        pass

