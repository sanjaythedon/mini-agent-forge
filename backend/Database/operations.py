from Database.interfaces import TableOperations, DataOperationsWithoutDelete, Database


class DatabaseTableManager(TableOperations):
    """Handles PostgreSQL table operations."""
    
    def __init__(self, connection_manager):
        self.connection_manager = connection_manager
    
    def create_table(self, table_name, columns):
        """
        Create a table in the database.
        
        Args:
            table_name: Name of the table to create
            columns: Dictionary of column names and data types
        
        Returns:
            True if table was created successfully, False otherwise
        """
        try:
            cursor = self.connection_manager.get_cursor()
            if not cursor:
                return False
                
            columns_str = ", ".join([f"{col_name} {data_type}" for col_name, data_type in columns.items()])
            query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str})"
            
            cursor.execute(query)
            self.connection_manager.commit()
            return True
        except psycopg2.Error as e:
            print(f"Error creating table {table_name}: {e}")
            return False


class DatabaseDataManager(DataOperationsWithoutDelete):
    """Handles PostgreSQL data operations."""
    
    def __init__(self, placeholder_string, connection_manager):
        super().__init__(placeholder_string)
        self.connection_manager = connection_manager
    
    def insert(self, table_name, data):
        """
        Insert data into a table.
        
        Args:
            table_name: Name of the table to insert data into
            data: Dictionary of column names and values to insert
        
        Returns:
            ID of the inserted row, or None if insertion failed
        """
        try:
            cursor = self.connection_manager.get_cursor()
            if not cursor:
                return None
                
            columns = list(data.keys())
            values = list(data.values())
            
            placeholders = ", ".join([self.placeholder_string for _ in columns])
            
            columns_str = ", ".join(columns)
            query = f"INSERT INTO {table_name} ({columns_str}) VALUES ({placeholders})"
            
            cursor.execute(query, values)
            self.connection_manager.commit()
            
            return cursor.lastrowid
        except psycopg2.Error as e:
            print(f"Error inserting into table {table_name}: {e}")
            return None
    
    def read(self, table_name, columns=None, condition=None, condition_values=None):
        """
        Read data from a table.
        
        Args:
            table_name: Name of the table to read data from
            columns: List of column names to select, or None to select all columns
            condition: SQL condition to filter rows, or None to select all rows
            condition_values: Values to use in the condition, or None if no condition is specified
        
        Returns:
            List of dictionaries containing the selected data
        """
        try:
            cursor = self.connection_manager.get_cursor()
            if not cursor:
                return []
                
            if columns:
                columns_str = ", ".join(columns)
            else:
                columns_str = "*"
            query = f"SELECT {columns_str} FROM {table_name}"
            
            if condition:
                query += f" WHERE {condition}"
                
            if condition_values:
                cursor.execute(query, condition_values)
            else:
                cursor.execute(query)
                
            results = cursor.fetchall()
            
            if columns:
                column_names = columns
            else:
                column_names = [description[0] for description in cursor.description]
                
            formatted_results = []
            for row in results:
                row_dict = {}
                for i, value in enumerate(row):
                    row_dict[column_names[i]] = value
                formatted_results.append(row_dict)
                
            return formatted_results
        except psycopg2.Error as e:
            print(f"Error reading from table {table_name}: {e}")
            return []
    
    def update(self, table_name, data, condition, condition_values):
        """
        Update data in a table.
        
        Args:
            table_name: Name of the table to update data in
            data: Dictionary of column names and values to update
            condition: SQL condition to filter rows to update
            condition_values: Values to use in the condition
        
        Returns:
            Number of rows updated
        """
        try:
            cursor = self.connection_manager.get_cursor()
            if not cursor:
                return 0
                
            set_clause = ", ".join([f"{column} = {self.placeholder_string}" for column in data.keys()])
            
            query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
            print(query)

            
            values = list(data.values()) + list(condition_values)
            print(values)
            
            cursor.execute(query, values)
            self.connection_manager.commit()
            
            return cursor.rowcount
        except psycopg2.Error as e:
            print(f"Error updating table {table_name}: {e}")
            return 0


class DatabaseOperations(Database):
    """Database implementation using composition of specialized components."""
    
    def __init__(self, connection_manager=None, 
                 table_manager=None, data_manager=None):
        """Initialize the DatabaseOperations.
        
        Args:
            connection_manager (PostgresConnection, optional): Custom connection manager
            table_manager (PostgresTableManager, optional): Custom table manager
            data_manager (PostgresDataManager, optional): Custom data manager
        """
        
        self.connection_manager = connection_manager
        self.table_manager = table_manager
        self.data_manager = data_manager
        
        self.connect()
    
    def connect(self):
        """Connect to the database."""
        return self.connection_manager.connect()
    
    def close(self):
        """Close the database connection."""
        self.connection_manager.close()
    
    def create_table(self, table_name, columns):
        """Create a table in the database."""
        return self.table_manager.create_table(table_name, columns)
    
    def insert(self, table_name, data):
        """Insert data into a table."""
        return self.data_manager.insert(table_name, data)
    
    def read(self, table_name, columns=None, condition=None, condition_values=None):
        """Read data from a table."""
        return self.data_manager.read(table_name, columns, condition, condition_values)
    
    def update(self, table_name, data, condition, condition_values):
        """Update data in a table."""
        return self.data_manager.update(table_name, data, condition, condition_values)
