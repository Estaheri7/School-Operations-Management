from databases.mysql_connector import MySQLConnector
from databases.table_queries import tables
import json

with open("databases/db_info.json", "r") as file:
    db_info = json.load(file)
db = MySQLConnector(db_info["host"], db_info["user"], db_info["password"])
db.create_database(db_info["db_name"])
db.create_tables(table_queries=tables)
