from abc import ABCMeta, abstractmethod

"""
    Abstract class for connecting to databases. 
    Known descendant: DatabaseConnectionInfux
"""


class DatabaseConnection(object):
    def __init__(self, db_name):
        self.db_name = db_name
        self.client = None



    @abstractmethod
    def db_exists(self, name):
        pass

    @abstractmethod
    def query_database(self, query):
        pass

    @abstractmethod
    def import_restful_api_response(self, data_points_json):
        pass



