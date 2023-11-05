from tax_calculator import TaxCalculator
from format_handler import CentRounder

class PayCalculator:
    def __init__(self, hourly_rate: int, hours_worked: int, tfn: int, threshold_claimed: bool, residence: str):
        self.gross_pay = self.__calculate_gross(hourly_rate, hours_worked)
        self.tax_amount = self.__calculate_tax(tfn, threshold_claimed, residence)
        self.super_amount = self.__calculate_super()
        self.results = self.__calculate_results()

    def __calculate_gross(self, hourly_rate: int, hours_worked: int):
        """
        Get the weekly gross pay for an employee.

        Parameters:
            hourly_rate: The hourly rate for an employee in AUD
            hours_worked: The amount of hours worked by an employee for the week

        Returns:
            gross_pay(int): The weekly gross pay calculated with the formula `hourly rate * hours worked`
        """
        gross_pay = hourly_rate * hours_worked
        return gross_pay
    
    def __calculate_tax(self, tfn: int, threshold_claimed: bool, residence: str):
        """
        Get the tax amount by passing parameters to the TaxCalculator class to determine the correct tax formula.

        Parameters:
            tfn: The Tax File Number of an employee (may be null)
            threshold_claimed: A record of if an employee has claimed the tax-free threshold (may be null)
            residence: The country of residence for an employee
        
        Returns:
            tax_amount(float): The weekly tax amount calculated with one of two formulas: `rounded gross pay * tax rate` or `coefficient A * (gross pay + 99 cents) - coefficient B`
        """
        gross_pay = self.gross_pay

        tax_calculator = TaxCalculator(gross_pay, tfn, threshold_claimed, residence)
        tax_rate = tax_calculator.tax_rate

        if isinstance(tax_rate, float):
            pay_rounded = round(gross_pay)
            tax_amount = pay_rounded * tax_rate
            return tax_amount
        else:
            coef_a, coef_b = tax_rate

            tax_amount = coef_a * (gross_pay + 0.99) - coef_b
            return tax_amount

    def __calculate_super(self):
        """
        Get the superannuation amount using the current super guarantee percentage.

        Returns:
            superannuation(float): The weekly superannuation amount calculated with the formula `(gross pay * super percentage) / 100`
        """
        gross_pay = self.gross_pay

        super_percentage = 11

        superannuation = (gross_pay * super_percentage) / 100
        return superannuation
    
    def __calculate_results(self):
        """
        Get the weekly net pay and pass all calculation results to the CentRounder class.

        Returns:
            rounded_results(tuple[str, str, str, str]): The calculation results for gross pay, tax, superannuation and net pay, rounded to 2 decimal places
        """
        gross_pay = self.gross_pay
        tax_amount = self.tax_amount
        superannuation = self.super_amount

        net_pay = gross_pay - tax_amount - superannuation

        results = [gross_pay, tax_amount, superannuation, net_pay]

        cent_rounder = CentRounder(results)
        rounded_results = cent_rounder.rounded_results

        return rounded_results
