from pyodbc import Cursor
from file_handler import QueryReader
from format_handler import PlaceholderHandler

class PaySummary:
    def __init__(self, cursor: Cursor, file_name: str):
        self.query_result = self.__execute_query(cursor, file_name)

    def __execute_query(self, cursor: Cursor, file_name: str):
        """
        Get a list of all the results from an executed query.

        Parameters:
            cursor: The database cursor returned from the pyodbc server connection
            file_name: The name of the .sql file to pass to the QueryReader class

        Returns:
            result(list): A list of the pay summary data for each employee
        """
        file_path = QueryReader(file_name)
        query = file_path.query
        cursor.execute(query)

        output = cursor.fetchall()
        result = []

        for row in output:
            result.append(row)
        
        return result

class Employee:
    def __init__(self, cursor: Cursor, file_name: str, id: int):
        self.updated_query = self.__format_query(file_name, id)
        self.query_result = self.__execute_query(cursor)

    def __format_query(self, file_name: str, id: int):
        """
        Replace the placeholder ID in the query with the ID selected by the user.

        Parameters:
            file_name: The name of the .sql file to pass to the QueryReader class
            id: The employee ID selected from the pay summary list
        
        Returns:
            updated_query(string): The new SQL query string with the updated employee ID
        """
        file_path = QueryReader(file_name)
        query_string = file_path.query

        query = PlaceholderHandler(query_string, id)
        updated_query = query.updated_string
        return updated_query

    def __execute_query(self, cursor: Cursor):
        """
        Get a single result from an executed query.

        Parameters:
            cursor: The database cursor returned from the pyodbc server connection
        
        Returns:
            result(Row): Employee details and tax data for an individual employee
        """
        query = self.updated_query
        cursor.execute(query)

        result = cursor.fetchone()
        return result
