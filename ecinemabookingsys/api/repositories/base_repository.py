"""
Base Repository - Abstract base class for all data access objects.

The Repository pattern separates data access logic from business logic.
All repositories inherit from this base and implement specific queries for their domain objects.
"""

from abc import ABC, abstractmethod
from db import get_db


class BaseRepository(ABC):
    """
    Abstract base repository providing common data access patterns.

    Concrete repositories inherit from this and implement entity-specific queries.
    Key principle: A repository returns domain objects, never raw dicts.
    """

    def __init__(self):
        """Initialize repository - subclasses don't need to override this."""
        pass

    @staticmethod
    def get_db():
        """Get database connection."""
        return get_db()

    @abstractmethod
    def find_by_id(self, entity_id):
        """
        Find entity by ID.
        Returns: Domain object or None
        """
        pass

    @abstractmethod
    def save(self, entity):
        """
        Save entity (insert or update).
        Takes: Domain object
        Returns: Saved entity with ID populated
        """
        pass

    @abstractmethod
    def delete(self, entity):
        """
        Delete entity.
        Takes: Domain object
        Returns: True if successful
        """
        pass

    @abstractmethod
    def get_all(self):
        """
        Get all entities.
        Returns: List of domain objects
        """
        pass


class CRUDRepository(BaseRepository):
    """
    Generic CRUD repository with common SQL patterns.
    Subclasses implement mapping fromSQL rows to domain objects.
    """

    def __init__(self):
        super().__init__()

    @staticmethod
    def execute_query(query, params=None):
        """Execute a SELECT query and return results."""
        conn = BaseRepository.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def execute_query_one(query, params=None):
        """Execute a SELECT query and return single result."""
        conn = BaseRepository.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                return cursor.fetchone()
        finally:
            conn.close()

    @staticmethod
    def execute_update(query, params=None):
        """Execute INSERT/UPDATE/DELETE query."""
        conn = BaseRepository.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.rowcount
        finally:
            conn.close()

    @staticmethod
    def execute_insert_get_id(query, params=None):
        """Execute INSERT and return generated ID."""
        conn = BaseRepository.get_db()
        try:
            with conn.cursor() as cursor:
                cursor.execute(query, params or ())
                conn.commit()
                return cursor.lastrowid
        finally:
            conn.close()
