import os
import sys
import csv
import exceptions
from codecs import open

class QueryReader:
    def __init__(self, file_name: str):
        self.query = self.__read_file(file_name)

    def __read_file(self, file_name: str):
        """
        Get the current working directory and read the SQL file at the specified location.

        Parameters:
            file_name: The SQL file to read
        
        Returns:
            query(str): The query string from the SQL file
        
        Exceptions:
            exceptions.FileNotFoundError: The file couldn't be read because it wasn't in the specified location
        """
        sql_file = 'res/' + file_name + '.sql'

        if getattr(sys, 'frozen', False):
            working_directory = os.path.dirname(sys.executable)
        elif __file__:
            working_directory = os.path.dirname(__file__)

        file_path = os.path.join(working_directory, sql_file)

        try:
            query = open(file_path, mode='r', encoding='utf-8-sig').read()
            return query

        except FileNotFoundError as error:
            raise exceptions.FileNotFoundError(error)

class CsvReader:
    def __init__(self, file_name: str, comparison_variable: int):
        self.row_result = self.__read_file(file_name, comparison_variable)

    def __read_file(self, file_name: str, comparison_variable: int):
        """
        Get the current working directory and read the CSV file at the specified location.

        Iterate through each row in the CSV until `comparison variable < upper earnings limit` then assign coefficients A and B to the corresponding row indexes.

        Parameters:
            file_name: The CSV file to read
            comparison_variable: The gross pay result passed from the PayCalculator class
        
        Returns:
            `coef_a` and `coef_b` as floats
        """
        csv_file = 'res/' + file_name + '.csv'

        if getattr(sys, 'frozen', False):
            working_directory = os.path.dirname(sys.executable)
        elif __file__:
            working_directory = os.path.dirname(__file__)

        file_path = os.path.join(working_directory, csv_file)

        with open(file_path) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            line_count = 0

            for row in csv_reader:
                if line_count == 0:
                    line_count += 1
                else:
                    upper_limit = float(row[0])
                    coef_a = float(row[1])
                    coef_b = float(row[2])

                    line_count += 1

                    if comparison_variable < upper_limit:
                        return coef_a, coef_b

class CsvWriter:
    def __init__(self, file_path: str, payslip_data: list):
        self.exported_file = self.__write_file(file_path, payslip_data)

    def __write_file(self, file_path: str, payslip_data: list):
        """
        Assign header values and write the header values and payslip data values to a CSV file.

        Parameters:
            file_path: The export location and templated file name
            payslip_data: The employee payslip data values
        """
        header = ['Employee ID', 'First Name', 'Last Name', 'Date Submitted', \
                  'Gross Pay', 'Tax Amount', 'Superannuation', 'Net Pay']

        with open(file_path, mode='w') as csv_file:
            csv_writer = csv.writer(csv_file)
            csv_writer.writerow(header)
            csv_writer.writerow(payslip_data)
        