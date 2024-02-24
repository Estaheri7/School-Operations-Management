from databases import MySQLConnector


def create_tables(db_manager: MySQLConnector, table_query: dict):
    for query in table_query.values():
        db_manager.create_table(query)
