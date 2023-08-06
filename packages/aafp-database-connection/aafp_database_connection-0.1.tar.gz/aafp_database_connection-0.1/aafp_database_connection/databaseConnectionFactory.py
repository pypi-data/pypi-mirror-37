# Polymorphic factory methods.
from __future__ import generators
from database_connection.databaseConnectionInflux import DatabaseConnectionInflux


class DatabaseConnectionFactory:
    factories = {}

    def add_factory(id, db_conn_factory):
        DatabaseConnectionFactory.factories.put[id] = db_conn_factory
    add_factory = staticmethod(add_factory)

    # A Template Method:
    def create_database_connection(db_type, db_name, host, port, user, password):
        if db_type not in DatabaseConnectionFactory.factories:
            DatabaseConnectionFactory.factories[db_type] = eval('DatabaseConnection' + db_type.title() +  '.Factory()')
        return DatabaseConnectionFactory.factories[db_type].create(db_name, host, port, user, password)

    create_database_connection = staticmethod(create_database_connection)