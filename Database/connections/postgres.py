import psycopg2
from Database.interfaces import Connection

class PostgresConnection(Connection):
    """Handles PostgreSQL connection management."""
    
    def __init__(self, host, port, user, password, database):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
    
    def connect(self):
        """Establish connection to PostgreSQL database."""
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database
            )
            self.cursor = self.connection.cursor()
            return True
        except psycopg2.Error as e:
            print(f"Database connection error: {e}")
            return False
    
    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()
            self.connection = None
            self.cursor = None
    
    def get_cursor(self):
        """Get the current cursor."""
        return self.cursor
    
    def commit(self):
        """Commit the current transaction."""
        if self.connection:
            self.connection.commit()
    
    def __del__(self):
        """Ensure connection is closed when object is destroyed."""
        self.close()