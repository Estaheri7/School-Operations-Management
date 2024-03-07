from databases.mysql_connector import MySQLConnector
from databases.table_queries import tables
import json

# By importing this file to main and using MySQLConnector class we create fresh database and tables.
# We can use db variable later in main file.

with open("databases/db_info.json", "r") as file:
    db_info = json.load(file)
db = MySQLConnector(db_info["host"], db_info["user"], db_info["password"])
db.create_database(db_info["db_name"])
db.create_tables(table_queries=tables)
