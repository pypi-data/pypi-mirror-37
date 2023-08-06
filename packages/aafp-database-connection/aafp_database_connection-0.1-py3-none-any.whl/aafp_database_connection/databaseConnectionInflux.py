from influxdb import InfluxDBClient
from database_connection.databaseConnection import DatabaseConnection


class DatabaseConnectionInflux(DatabaseConnection):

    def __init__(self, db_name, host='localhost', port=8086, user='root', password='root'):
        """
            Return an InfluxDBClient object which represents a connection to an InfluxDBClient object.

            :param db_name: name of the database to be connected to
            :type db_name: str
            :param host: name of host server
            :type host: str
            :param port: port number used by database, on the host server. Default 8086
            :type port: integer
            :param user: user name used to log in to db. Default = 'root'
            :type user: str
            :param password the password used to log in to db. Default = 'root'
            :type password str

            :raises ConnectionError if fails to connect for any reason


            :side-effect If the database connection is found, but there is no database with the name db_name, a database with that
            name will be created.

        """
        """"""
        super(DatabaseConnectionInflux, self).__init__(db_name)

        self.host = host
        self.port = port
        self.user = user
        self.password = password

        try:
            self.client = InfluxDBClient(host, port, user, password)
        except Exception as err:
            raise ConnectionError(
                "Error connecting to InfluxDB client at: host: " + str(host) + "; on port: " + str(port) +
                '; Error Msg: ' + err)

        if not self.db_exists(db_name):
            self.client.create_database(self.db_name)
        self.client.switch_database(self.db_name)

    class Factory:
        def create(self, db_name, host, port, user, password):
            return DatabaseConnectionInflux(db_name, host, port, user, password)


    def db_exists(self, db_name):
        """
            Returns true if a database with the name db_name exists in the influxdb connection and False otherwise.

            :param db_name: db name to be searched for
            :type db_name: str
        """
        for db in self.client.get_list_database():
            if db['name'] == db_name:
                return True
        return False

    def measurement_exists(self, measurement_name):
        """
            Returns true if a measurement with the name measurement_name exists in the db and False otherwise.

            :param measurement_name: measurement name to be searched for
            :type measurement_name: str
        """
        measurement_list = self.client.get_list_measurements()
        for measurement in measurement_list:
            if measurement['name'] == measurement_name:
                return True
        return False

    def drop_database(self, db_name):
        self.client.drop_database(db_name)

    def query_database(self, query):
        """
            Queries a database  by running the query .

            :param query: influxdb query string
            :type query: str

            :returns resultset of query
        """
        try:
            result = self.client.query(query)
        except Exception as err:
            raise ConnectionError(
                "Error querying InfluxDB client: " + str(err))
        return result

    def import_json(self, data_points_json):
        """
            Inports datapoints into influxdb datbase that are in json format

            :param data_points_json: datapoints to be added in the correct json format
            :type data_points_json: json

            :raises ConnectionError if any erro connecting to database, with error message from influxd connection.
        """
        try:
            self.client.write_points(data_points_json, time_precision='s')
        except Exception as err:
            raise ConnectionError("Error importing to InfluxDB database" + self.db_name + ": " + str(err))