from sqlmodel import Session, create_engine
from typing import Generator
from contextlib import contextmanager

from app.config.settings import DATABASE_URL, ECHO_SQL

# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, echo=ECHO_SQL)

@contextmanager
def get_session() -> Generator[Session, None, None]:
    """
    Provide a transactional scope around a series of operations.
    
    Usage:
        with get_session() as session:
            session.add(some_object)
            session.commit()
    """
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()

def get_db_session():
    """
    Get database session for dependency injection.
    """
    with get_session() as session:
        yield session
