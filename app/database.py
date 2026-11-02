import os
from contextlib import contextmanager
from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker, scoped_session
from app.config import Config

# Base declarative class for ORM models
Base = declarative_base()

# Engine setup
engine = create_engine(
    Config.SQLALCHEMY_DATABASE_URI,
    **Config.SQLALCHEMY_ENGINE_OPTIONS
)

# Thread-safe scoped session
SessionLocal = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

@contextmanager
def get_db():
    """Context manager for SQLAlchemy ORM sessions."""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

def execute_raw_sql(sql_query, params=None, fetch_all=True, commit=False):
    """
    Execute raw SQL queries using SQLAlchemy engine connection.
    Demonstrates pure SQL execution for educational and analytical purposes.
    Returns: list of dicts for SELECT, or rowcount for DML.
    """
    params = params or {}
    with engine.connect() as conn:
        with conn.begin() if commit else nullcontext():
            result = conn.execute(text(sql_query), params)
            if commit:
                pass # conn.begin() commits on exit
            if result.returns_rows:
                if fetch_all:
                    columns = result.keys()
                    rows = result.fetchall()
                    return [dict(zip(columns, row)) for row in rows]
                else:
                    row = result.fetchone()
                    return dict(zip(result.keys(), row)) if row else None
            return result.rowcount

class nullcontext:
    """Fallback context manager for non-commit connections."""
    def __enter__(self):
        return None
    def __exit__(self, exc_type, exc_val, exc_tb):
        return False
