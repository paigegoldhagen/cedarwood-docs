import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

from pyodbc import Cursor

from connect_database import DatabaseConnection
from query_database import PaySummary, Employee
from format_handler import StringFormatter
from pay_calculator import PayCalculator
from file_handler import CsvWriter

class InitialiseWindow:
    def __init__(self):
        """
        Call the main loop of Tkinter to show the app window.
        """
        window = tk.Tk()
        main = MainView(window)
        main.pack(side='top', fill='both', expand=True)
        window.wm_geometry('400x350')
        window.title('Cedarwood')
        window.mainloop()

class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
    def show(self):
        """
        Raise the current page in the viewing stack.
        """
        self.lift()

class PayslipView(Page):
    def __init__(self, cursor: Cursor, id: int):
        """
        Get an employee record from the employee query, passing the results to the PayCalculator class, and displaying all results.

        Load the GUI elements - subtitle label, date label, basic info label, hours label, tax label, pay info label, export button, back button.

        Parameters:
            cursor: The database cursor used for executing queries in the Employee class
            id: The employee ID to use in the query string
        """
        Page.__init__(self)

        self.gui_objects = []
        self.database_cursor = cursor

        file_name = 'employee_information'

        employee_data = Employee(cursor, file_name, id)
        query_result = employee_data.query_result

        employee_id, first_name, last_name, hourly_rate, country, \
        tfn, threshold_claimed, hours_worked, date_submitted = query_result

        self.file_name_template = 'payslip_' + first_name + last_name + '_' + str(date_submitted)
        full_name = first_name + ' ' + last_name

        subtitle = tk.Label(self, text='Payslip for '+ full_name)
        date_info = tk.Label(self, text='Date submitted: ' + str(date_submitted))

        basic_info = tk.Label(self, text='Employee ID: ' + str(employee_id) + 
                                   '\nName: ' + full_name +
                                   '\nHourly rate: ' + str(hourly_rate) + ' AUD')

        hours_info = tk.Label(self, text='Hours worked this week: ' + str(hours_worked))

        tax_info = tk.Label(self, text='TFN: ' + str(tfn) +
                                 '\nTax threshold claimed: ' + str(threshold_claimed) +
                                 '\nCountry of residence: ' + country)

        pay_calculator = PayCalculator(hourly_rate, hours_worked, tfn, threshold_claimed, country)
        gross_pay, tax_amount, superannuation, net_pay = pay_calculator.results

        self.payslip_data = [employee_id, first_name, last_name, date_submitted, \
                             gross_pay, tax_amount, superannuation, net_pay]

        pay_info = tk.Label(self, text='Gross pay: ' + str(gross_pay) + ' AUD' + 
                                 '\nTax amount: ' + str(tax_amount) + ' AUD' +
                                 '\nSuperannuation: ' + str(superannuation) + ' AUD' +
                                 '\nNet pay: ' + str(net_pay) + ' AUD')

        export_button = tk.Button(self, text='Export as .csv', command=self.__export_payslip)
        back_button = tk.Button(self, text='Go back', command=self.__go_back)

        self.gui_objects.extend([subtitle, date_info, basic_info, \
                                 hours_info, tax_info, pay_info,  \
                                 export_button, back_button])
        
        for object in self.gui_objects:
            object.pack()

    def __export_payslip(self):
        """
        Export the query and calculator results to CSV by using the CsvWriter class and asking the user for an export directory.

        Show a confirmation message if the file was exported successfully.
        """
        export_location = filedialog.askdirectory()
        file_name = self.file_name_template

        file_path = export_location + '/' + file_name + '.csv'

        CsvWriter(file_path, self.payslip_data)
        messagebox.showinfo('Payslip exported', 'The payslip was exported to:\n' + file_path)

    def __go_back(self):
        """
        Go back to the Summary view.
        """
        summary = SummaryView(self.database_cursor)

        container = tk.Frame(self)
        container.pack(fill='both', expand=True)

        summary.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        for object in self.gui_objects:
            object.pack_forget()

        summary.show()

class SummaryView(Page):
    def __init__(self, cursor: Cursor):
        """
        Display a selectable list of results from the pay summary query.

        Load the GUI elements - subtitle label, listbox, generate button, logout button, format legend label.

        Parameters:
            cursor: The database cursor used for executing queries in the PaySummary class
        """
        Page.__init__(self)

        self.gui_objects = []
        self.database_cursor = cursor
        self.selected_index = None

        file_name = 'pay_summary'

        pay_summary = PaySummary(cursor, file_name)
        query_result = pay_summary.query_result

        self.subtitle = tk.Label(self, text='Weekly pay summary')
        self.subtitle.pack()

        summary_variable_object = tk.Variable(value=query_result)
        self.selectable_list = tk.Listbox(self, 
                                     listvariable=summary_variable_object,
                                     selectmode=tk.BROWSE)
        
        self.selectable_list.pack(fill='both', expand=True)
        self.selectable_list.bind('<<ListboxSelect>>', self.__record_selected)

        generate_button = tk.Button(self, text='Generate a payslip', command=self.__switch_view)
        logout_button = tk.Button(self, text='Log out', command=self.__go_back)
        legend = tk.Label(self, text="Format: (ID, 'First name', 'Last name', Hours worked)")

        self.gui_objects.extend([generate_button, logout_button, legend])

        for object in self.gui_objects:
            object.pack()

    def __record_selected(self, event):
        """
        Get the row selected from the listbox and determine the employee ID using the StringFormatter class.

        Parameters:
            event: The binding event that triggers this function - in this case, the binding sequence is `<<ListBoxSelect>>`
        """
        widget = event.widget
        self.selected_index = widget.curselection()
        selected_record = widget.get(self.selected_index[0])

        string_formatter = StringFormatter(selected_record)
        individual_entries = string_formatter.individual_entries
        self.employee_id = individual_entries[0]

    def __switch_view(self):
        """
        Show an error message if the user tries to generate a payslip without an employee selected, otherwise load the Payslip view.
        """
        if not self.selected_index:
            messagebox.showerror('Error', 'Please select an employee')
        else:
            container = tk.Frame(self)
            container.pack(fill='both', expand=True)

            payslip = PayslipView(self.database_cursor, self.employee_id)
            payslip.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

            self.subtitle.pack_forget()
            self.selectable_list.pack_forget()

            for object in self.gui_objects:
                object.pack_forget()
            
            payslip.show()

    def __go_back(self):
        """
        Go back to the Login view.
        """
        login = LoginView(self)

        container = tk.Frame(self)
        container.pack(fill='both', expand=True)

        login.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        self.subtitle.pack_forget()
        self.selectable_list.pack_forget()

        for object in self.gui_objects:
            object.pack_forget()

        login.show()

class LoginView(Page):
    def __init__(self, *args, **kwargs):
        """
        Load the GUI elements - username entry, password entry, login button.
        """
        Page.__init__(self, *args, **kwargs)
        self.gui_objects = []

        self.username_input = tk.Entry(self)
        self.password_input = tk.Entry(self, show='*')

        login_button = tk.Button(self, text='Log in', command=self.__login)

        self.gui_objects.extend([self.username_input, self.password_input, login_button])

        for object in self.gui_objects:
            object.pack()
    
    def __login(self):
        """
        Get the user inputs to pass to the DatabaseConnection class, pass the resulting database cursor to the Summary view, and load the Summary view.
        """
        username_string = self.username_input.get()
        password_string = self.password_input.get()

        if not username_string or not password_string:
            messagebox.showerror('Error', 'Please enter username and password')

        database = DatabaseConnection(username_string, password_string)
        database_cursor = database.connection

        container = tk.Frame(self)
        container.pack(fill='both', expand=True)

        summary = SummaryView(database_cursor)
        summary.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        for object in self.gui_objects:
            object.pack_forget()

        summary.show()

class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        """
        Determine which GUI elements should appear in all views and load the Login view.
        """
        tk.Frame.__init__(self, *args, **kwargs)

        login = LoginView(self)

        title_frame = tk.Frame(self)
        container = tk.Frame(self)

        title_frame.pack()
        container.pack(fill='both', expand=True)

        login.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        title = tk.Label(title_frame, text='🌳\nCedarwood')
        title.pack(side='top', fill='both', expand=True)

        login.show()

InitialiseWindow()