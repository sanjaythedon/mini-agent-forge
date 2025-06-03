from dotenv import load_dotenv
from Database.operations import DatabaseOperations, DatabaseTableManager, DatabaseDataManager
from Database.connections import PostgresConnection
import os

load_dotenv()
connection_manager = PostgresConnection(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB")
    )
table_manager = DatabaseTableManager(connection_manager)
data_manager = DatabaseDataManager("%s", connection_manager)
db = DatabaseOperations(connection_manager=connection_manager, table_manager=table_manager, data_manager=data_manager)
# db.create_table("test", {"id": "SERIAL PRIMARY KEY", "name": "TEXT"})
# db.insert("test", {"name": "test"})
# print(db.read("test"))
# db.update("test", {"name": "test2"}, "id = %s", [1])
print(db.read("prompt_log"))
