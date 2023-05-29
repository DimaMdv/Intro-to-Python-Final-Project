'''
  Name : ATM Simulator
  
  Description: An app that simulates using an ATM.

  Instructor: Mohammad Morovati
  Author: Medvedkov Dmytro
  Version: 1
  Class: CIS2531
  Section: NET02
  Assignment#: Final Project
  Date: 08/05/2022
''' 


'''Imports'''
import tkinter, tkinter.messagebox, sqlite3
from Accounts import *


'''Classes'''
class GUI:
    def __init__(self):
        #actributes for the app to work correctly
        self.database = sqlite3.connect("BankAccounts.db")

        self.main_window = tkinter.Tk() #the main window where user will perform actions with accounts
        self.main_window.title("ATM Simulator Login")
        self.main_window.geometry("230x200")

        #frames for login 
        self.login_user_input_frame = tkinter.Frame(self.main_window).grid()
        self.login_button_frame = tkinter.Frame(self.main_window).grid()
        #frames for main operations
        self.main_user_info_frame = tkinter.Frame(self.main_window).grid()
        self.main_user_input_frame = tkinter.Frame(self.main_window).grid()
        self.main_buttons_frame = tkinter.Frame(self.main_window).grid()

        #widgets for login screen
        self.__build_id_form()
        self.__build_pin_form()
        self.__build_confirm_button()
        self.__build_quit_button()

        # Entering the tkinter main loop.
        tkinter.mainloop()

    #login Widgets
    def __build_id_form(self): #prompts and accemp user's pin
        self.id_prompt_label = tkinter.Label(self.login_user_input_frame, text="Enter your ID")
        self.id_prompt_label.grid(column=1, row=4, pady=5, padx=5)
        self.id_entry = tkinter.Entry(self.login_user_input_frame, width=8)
        self.id_entry.grid(column=1, row=5, pady=5, padx=5)

    def __build_pin_form(self): #prompts and accepts user's pin
        self.pin_prompt_label = tkinter.Label(self.login_user_input_frame, text="Enter your PIN")
        self.pin_prompt_label.grid(column=1, row=6, pady=5, padx=5)
        self.pin_entry = tkinter.Entry(self.login_user_input_frame, show="*", width=8)
        self.pin_entry.grid(column=1, row=7, pady=5, padx=5)

    def __build_confirm_button(self): #button used to advance into the app
        self.confirm_button = tkinter.Button(self.login_button_frame, text="Confirm", command=self.does_Account_Exists)
        self.confirm_button.grid(column=0, row=8, pady=5, padx=5)

    def __build_quit_button(self): #button used to close the app
        self.quit_button = tkinter.Button(self.login_button_frame, text='Quit', fg='red',command=self.main_window.destroy)
        self.quit_button.grid(column=2, row=8, pady=5, padx=5)

    #main widgets
    def __build_user_info(self): #text used to infor user about account status
        self.checking_var = tkinter.StringVar()
        self.saving_var = tkinter.StringVar()

        self.name_lable = tkinter.Label(self.main_user_info_frame, text=f"Hello {self.UserAccount.getFirstName()} {self.UserAccount.getSecondName()}!") #there is no need to update the name, so this text is unchanged
        self.Checking_lable = tkinter.Label(self.main_user_info_frame, textvariable=self.checking_var)
        self.Saving_lable = tkinter.Label(self.main_user_info_frame, textvariable=self.saving_var)

        self.set_User_Info()
        
        self.name_lable.grid(column=0, row=0, columnspan=3, pady=5, padx=5)
        self.Checking_lable.grid(column=0, row=1, columnspan=3, pady=5, padx=5)
        self.Saving_lable.grid(column=0, row=2, columnspan=3, pady=5, padx=5)

    def __build_account_options(self): #avaible acount options
        self.account_chose_label = tkinter.Label(self.main_user_input_frame, text="Choose account to operate with")

        self.account_chose_label.grid(column=0, row=3, pady=5, padx=5)

        self.account_var = tkinter.IntVar()
        self.account_var.set(0) #the initial value

        self.Cheching_rb = tkinter.Radiobutton(self.main_user_input_frame, text="Checking account", variable=self.account_var, value=1)
        self.Saving_rb = tkinter.Radiobutton(self.main_user_input_frame, text="Saving account", variable=self.account_var, value=2)

        self.Cheching_rb.grid(column=0, row=4, pady=5, padx=5)
        self.Saving_rb.grid(column=0, row=5, pady=5, padx=5)

    def __build_amount_entry(self): #entry that accepts amount operated
        self.money_prompt_label = tkinter.Label(self.main_user_input_frame, text="Choose amount to operate with")
        self.money_amount_entry = tkinter.Entry(self.main_user_input_frame, width=15)

        self.money_prompt_label.grid(column=2, row=3, pady=5, padx=5)
        self.money_amount_entry.grid(column=2, row=4, pady=5, padx=5)

    def __build_buttons_label(self):
        self.button_prompt_label = tkinter.Label(self.main_user_input_frame, text="Choose the operation")

        self.button_prompt_label.grid(column=1, row=6, pady=5, padx=5)

    def __build_deposit_button(self): #button that invokes the depost sequence
        self.deposit_button = tkinter.Button(self.main_buttons_frame, text="Deposit", height=2, width=12, command=self.deposit_operation)

        self.deposit_button.grid(column=0, row=7, pady=5, padx=5)

    def __build_withdraw_button(self): #button that invokes the withdraw sequence
        self.withdraw_button = tkinter.Button(self.main_buttons_frame, text="Withdraw", height=2, width=12, command=self.withdraw_operation)

        self.withdraw_button.grid(column=2, row=7, pady=5, padx=5)

    def __build_exit_button(self): #button that exits to the login menue
        self.exit_button = tkinter.Button(self.main_buttons_frame, text='Finish and exit', fg='red',command=self.move_To_Login_Widgets)

        self.exit_button.grid(column=1, row=8, pady=5, padx=5)

    #methods
    def does_Account_Exists(self): #checks if account exists; if so, changes the window; if not displays the error message
        localCursor = self.database.cursor()
        localCursor.execute('''SELECT * FROM Accounts WHERE ID == ? AND PIN == ?''', (self.id_entry.get(), self.pin_entry.get()))
        account = localCursor.fetchall()
        if len(account) == 1:
            self.move_To_Main_Widgets()
        else:
            tkinter.messagebox.showerror(title="ERROR", message="Couldn't find account") #shows the error message

    def move_To_Main_Widgets(self):
        #changing the properties of the main window
        self.main_window.title("ATM Simulator")
        self.main_window.geometry("500x350")

        #Creating instances of all needed classes
        self.UserAccount = Account(self.id_entry.get(), self.database)
        self.UserAccount.setAttributes()
        self.UserChecking = CheckingAccount(self.id_entry.get(), self.database)
        self.UserChecking.setAttributes()
        self.UserSaving = SavingAccount(self.id_entry.get(), self.database)
        self.UserSaving.setAttributes()

        #hiding old widgets; we not destroying them because user will encounter this options again
        self.id_prompt_label.grid_forget()
        self.id_entry.grid_forget()
        self.pin_prompt_label.grid_forget()
        self.pin_entry.grid_forget()
        self.confirm_button.grid_forget()
        self.quit_button.grid_forget()

        #invoking new widgets
        self.__build_user_info()
        self.__build_account_options()
        self.__build_amount_entry()
        self.__build_buttons_label()
        self.__build_deposit_button()
        self.__build_withdraw_button()
        self.__build_exit_button()
        

    def move_To_Login_Widgets(self):
        #setting window to previous settings
        self.main_window.title("ATM Simulator Login")
        self.main_window.geometry("230x200")

        #destroying all objects
        del self.UserAccount
        del self.UserChecking
        del self.UserSaving

        #removing main widgets
        self.name_lable.grid_forget()
        self.Checking_lable.grid_forget()
        self.Saving_lable.grid_forget()
        self.account_chose_label.grid_forget()
        self.Cheching_rb.grid_forget()
        self.Saving_rb.grid_forget()
        self.money_prompt_label.grid_forget()
        self.money_amount_entry.grid_forget()
        self.button_prompt_label.grid_forget()
        self.deposit_button.grid_forget()
        self.withdraw_button.grid_forget()
        self.exit_button.grid_forget()

        #rebuilding login widgets
        self.__build_id_form()
        self.__build_pin_form()
        self.__build_confirm_button()
        self.__build_quit_button()

    def set_User_Info(self):
        checking_output = "Your current balance on Checking Account is " + str(self.UserChecking.getBalance()) + "."
        saving_output = "Your current balance on Saving Account is " + str(self.UserSaving.getBalance()) + " and your withdrawal limit is " + str(self.UserSaving.getWithdrawLimit()) + "."

        self.checking_var.set(checking_output)
        self.saving_var.set(saving_output)

    def deposit_operation(self): #method that is responsible for adding finances to account
        amount = self.money_amount_entry.get()
        account = self.account_var.get()
        try:
            #filtering user input
            amount = float(amount)
            if amount <= 0:
                raise ValueError
            
            if account == 0:
                raise ValueError
            elif account == 1:
                self.UserChecking.deposit(amount)
            elif account == 2:
                self.UserSaving.deposit(amount)
            tkinter.messagebox.showinfo(title="Success", message="The money was successfully added to the account") #succsess message
            self.set_User_Info() #updating info
        except:
            tkinter.messagebox.showerror(title="ERROR", message="Wrong amount! The input must be a number that greater then 0 and eather of accounts must be chosen!") #error message
        
    def withdraw_operation(self):  #method that is responsible for subtracting finances from account
        amount = self.money_amount_entry.get()
        account = self.account_var.get()
        try:
            #filtering user input
            amount = float(amount)
            if amount <= 0:
                raise ValueError
            
            if account == 0:
                raise ValueError
            elif account == 1:
                result = self.UserChecking.withdraw(amount) #"result" variable shows the responce of the method and what type of error to throw
            elif account == 2:
                result = self.UserSaving.withdraw(amount)

            if result == 1: #code for insufficient funds
                tkinter.messagebox.showerror(title="ERROR", message="Insufficient funds!")
            elif result == 2: #code for "out of limit"
                tkinter.messagebox.showerror(title="ERROR", message="You are out of your withdrawals. Check again later!")
            else:
                tkinter.messagebox.showinfo(title="Success", message="The money was successfully withdrawn from the account") #succsess message
                self.set_User_Info() #updating info
        except:
            tkinter.messagebox.showerror(title="ERROR", message="Wrong amount! The input must be a number that greater then 0 and eather of accounts must be chosen!")


'''Main'''
if __name__ == "__main__":
    AppGUI = GUI()
