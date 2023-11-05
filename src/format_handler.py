class StringFormatter:
    def __init__(self, query: str):
        self.individual_entries = self.__format_query(query)
    
    def __format_query(self, query: str):
        """
        Take out unnecessary symbols from the query string and split the query into individual string entries.

        Parameters:
            query: The query string to format
        
        Returns:
            individual_entries(list[str]): Each query value split from the query string at `, `
        """
        string_trim = query.strip('()')
        individual_entries = string_trim.split(', ')
        return individual_entries

class PlaceholderHandler:
    def __init__(self, query: str, id: int):
        self.updated_string = self.__replace_value(query, id)

    def __replace_value(self, query: str, id: int):
        """
        Find the placeholder value in the query string and replace it with the passed employee ID.

        Parameters:
            query: The query string to find the placeholder value from
            id: The employee ID to replace the placeholder value

        Returns:
            updated_string(str): The new query string with the replaced employee ID value
        """
        updated_string = query.replace('0000', id)
        return updated_string

class CentRounder:
    def __init__(self, calculator_results: tuple[str, str, str, str]):
        self.rounded_results = self.__round_decimal_place(calculator_results)

    def __round_decimal_place(self, calculator_results: tuple[str, str, str, str]):
        """
        Format each calculation result to 2 decimal places (as a string for GUI purposes only).

        Parameters:
            calculator_results: The gross pay, tax amount, superannuation and netpay results from the pay calculator
        
        Returns:
            The calculation results rounded to 2 decimal places
        """
        gross_pay = format(calculator_results[0], '.2f')
        tax_amount = format(calculator_results[1], '.2f')
        superannuation = format(calculator_results[2], '.2f')
        net_pay = format(calculator_results[3], '.2f')

        return gross_pay, tax_amount, superannuation, net_pay
