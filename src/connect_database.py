import pyodbc
import exceptions

class DatabaseConnection:
    def __init__(self, username, password):
        self.connection = self.__connect_database(username, password)

    def __connect_database(self, username: str, password: str):
        """
        Use a connection string with pyodbc to establish a connection to a local host database.

        Parameters:
            username: User input of the server login username
            password: User input of the server login password
        
        Returns:
            cursor(Cursor): A database cursor used for executing queries

        Exceptions:
            exceptions.ConnectionError: Failure to connect to the server (pyodbc OperationalError)
        """

        server = '127.0.0.1'
        database = 'Cedarwood'

        try:
            connection = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};\
                                        SERVER='+ server +';\
                                        DATABASE='+ database +';\
                                        ENCRYPT=yes;\
                                        UID='+ username + ';\
                                        PWD='+ password +';\
                                        TrustServerCertificate=yes')
            
            cursor = connection.cursor()

            return cursor
        
        except pyodbc.OperationalError as error:
            raise exceptions.ConnectionError(error)
