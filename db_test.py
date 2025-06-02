from dotenv import load_dotenv
from Database.postgres import PostgresDatabase, PostgresConnection, PostgresTableManager, PostgresDataManager
import os

load_dotenv()
connection_manager = PostgresConnection(
        host=os.getenv("POSTGRES_HOST"),
        port=os.getenv("POSTGRES_PORT"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        database=os.getenv("POSTGRES_DB")
    )
table_manager = PostgresTableManager(connection_manager)
data_manager = PostgresDataManager(connection_manager)
db = PostgresDatabase(connection_manager=connection_manager, table_manager=table_manager, data_manager=data_manager)
db.create_table("test", {"id": "SERIAL PRIMARY KEY", "name": "TEXT"})
db.insert("test", {"name": "test"})
print(db.read("test"))
db.update("test", {"name": "test2"}, "id = %s", [1])
print(db.read("test"))
