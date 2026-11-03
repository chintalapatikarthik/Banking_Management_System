import pytest
import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.config import Config
from app.database import engine, Base, get_db
from database.init_db import init_database

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'test-secret-key-1234'

@pytest.fixture(scope='session')
def app():
    # Set in-memory test database
    os.environ['DATABASE_URL'] = 'sqlite:///:memory:'
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
    # Only reset if running SQLite test database
    try:
        if 'sqlite' in str(engine.url):
            init_database(reset=True)
    except Exception as e:
        print(f"Error resetting database after test suite: {e}")

