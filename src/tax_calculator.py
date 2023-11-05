from file_handler import CsvReader

class TaxCalculator:
    def __init__(self, gross_pay: int, tfn: int, threshold_claimed: bool, residence: str):
        self.tax_rate = self.__get_rate(gross_pay, tfn, threshold_claimed, residence)

    def __get_rate(self, gross_pay: int, tfn: int, threshold_claimed: bool, residence: str):
        """
        Get the tax rate either as a float or as coefficients A and B.

        Parameters:
            gross_pay: The weekly gross pay for an employee
            tfn: The Tax File Number of an employee (may be null)
            threshold_claimed: A record of if an employee has claimed the tax-free threshold (may be null)
            residence: The country of residence for an employee

        Returns:
            tax_rate(float): If there is no tfn record, the tax rate is `0.4700` for Australian residents and `0.4500` for foreign residents
            coefficients(tuple[float, float]): If there is a tfn record, pass the file name and gross pay parameters to the CsvReader class to determine the tax table coefficients
        """
        if tfn is None:
            if residence != 'Australia':
                tax_rate = 0.4500
                return tax_rate
            else:
                tax_rate = 0.4700
                return tax_rate
        else:
            file_name = ''

            if residence != 'Australia':
                file_name = 'foreign_resident'
            else:
                tax_threshold = str(threshold_claimed).lower()
                file_name = 'threshold_' + tax_threshold

            csv_reader = CsvReader(file_name, gross_pay)
            coefficients = csv_reader.row_result
            return coefficients
