import pymysql
from flask import g
import threading

class DatabaseConnection:
    """Singleton database connection manager."""
    _instance = None
    _lock = threading.Lock()
    _connection = None
    _thread_local = threading.local()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(DatabaseConnection, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_connection(cls):
        """Get the current database connection (request-scoped via Flask g)."""
        try:
            # Try to get from Flask's g object (request-scoped)
            if not hasattr(g, 'db_connection') or g.db_connection is None:
                g.db_connection = cls._create_connection()
            return g.db_connection
        except RuntimeError:
            # Outside request context, use thread-local storage
            if not hasattr(cls._thread_local, 'connection') or cls._thread_local.connection is None:
                cls._thread_local.connection = cls._create_connection()
            return cls._thread_local.connection

    @staticmethod
    def _create_connection():
        """Create a new database connection."""
        return pymysql.connect(
            host="127.0.0.1",
            port=33306,
            user="root",
            password="mysqlpass",
            database="cinemaebooking",
            cursorclass=pymysql.cursors.DictCursor
        )

    @classmethod
    def close_connection(cls):
        """Close the current database connection."""
        try:
            if hasattr(g, 'db_connection') and g.db_connection is not None:
                g.db_connection.close()
                g.db_connection = None
        except RuntimeError:
            # Outside request context
            if hasattr(cls._thread_local, 'connection') and cls._thread_local.connection is not None:
                cls._thread_local.connection.close()
                cls._thread_local.connection = None

    @classmethod
    def close_all(cls):
        """Close all connections."""
        try:
            if hasattr(g, 'db_connection') and g.db_connection is not None:
                g.db_connection.close()
                g.db_connection = None
        except RuntimeError:
            pass

        if hasattr(cls._thread_local, 'connection') and cls._thread_local.connection is not None:
            cls._thread_local.connection.close()
            cls._thread_local.connection = None


def get_db():
    """Get database connection (backward compatible)."""
    return DatabaseConnection.get_connection()


def close_db(e=None):
    """Close database connection (for Flask teardown)."""
    DatabaseConnection.close_connection()
