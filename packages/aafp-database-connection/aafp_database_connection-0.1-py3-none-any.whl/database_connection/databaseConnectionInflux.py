from influxdb import InfluxDBClient
from database_connection.databaseConnection import DatabaseConnection


class DatabaseConnectionInflux(DatabaseConnection):

    def __init__(self, db_name, host='localhost', port=8086, user='root', password='root'):
        """Return an InfluxDBClient object which represents a connection to
        an InfluxDBClient object."""
        super(DatabaseConnectionInflux, self).__init__(db_name)

        self.host = host
        self.port = port
        self.user = user
        self.password = password

        try:
            self.client = InfluxDBClient(host, port, user, password)
        except:
            raise ConnectionError(
                "Error connecting to InfluxDB client at: host: " + str(host) + "; on port: " + str(port))

        if not self.db_exists(db_name):
            self.client.create_database(self.db_name)
        self.client.switch_database(self.db_name)

    class Factory:
        def create(self, db_name, host, port, user, password):
            return DatabaseConnectionInflux(db_name, host, port, user, password)


    def db_exists(self, db_name):
        for db in self.client.get_list_database():
            if db['name'] == db_name:
                return True
        return False

    def measurement_exists(self, measurement_name):
        measurement_list = self.client.get_list_measurements()
        for measurement in measurement_list:
            if measurement['name'] == measurement_name:
                return True
        return False

    def drop_database(self, db_name):
        self.client.drop_database(db_name)

    def query_database(self, query):
        try:
            result = self.client.query(query)
        except Exception as err:
            raise ConnectionError(
                "Error querying InfluxDB client: " + str(err))
        return result

    #ToDo: This method seems dedicated to the CV Dashboard. Move dashboard logic to dashboard code and make this more generic.
    def get_recorded_measurement_list(self):
        measurements = []

        try:
            query_result = self.query_database('SHOW MEASUREMENTS')
        except:
            raise ConnectionError(
                "Error querying InfluxDB client. Check client is running/available")

        for result_part in query_result:
            for measurement in result_part:
                query_str_2 = 'SELECT * FROM ' + measurement['name']  #+ ' WHERE time > now() - ' + str(previous_hours) + 'h'
                query_result_2 = self.query_database(query_str_2)
                list_result = list(query_result_2.get_points( measurement['name'] ))
                if 'href' in list_result[0]:
                    href = list_result[0]['href']
                else:
                    href = ''
                if 'orig_measurement' in list_result[0]:
                    orig_m = list_result[0]['orig_measurement']
                else:
                    orig_m = ''
                if 'query' in list_result[0]:
                    query = list_result[0]['query']
                else:
                    query = ''
                if len(list_result) > 0 and 'type' in list_result[0]:
                    measurements.append(
                            {'name':measurement['name'],
                             'type': list_result[0]['type'].strip().lower(),
                             'href': href,
                             'orig_measurement': orig_m,
                             'query': query})


        return measurements

    def import_json(self, data_points_json):
        try:
            self.client.write_points(data_points_json, time_precision='s')
        except Exception as err:
            raise ConnectionError("Error importing to InfluxDB database" + self.db_name + ": " + str(err))