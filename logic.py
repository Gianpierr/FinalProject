from PyQt6.QtWidgets import *
from gui import *
import random
import csv


class Logic(QMainWindow, Ui_BankRegistration):
    CSV_FILE = '.venv/lib/user_info.csv'
    user_info = {}

    def __init__(self) -> None:
        """This sets up the initial GUI"""
        super().__init__()
        self.setupUi(self)
        self.frame1.hide()
        self.frame2.hide()
        self.frame3.hide()
        self.enter_button.clicked.connect(lambda: self.enter())
        self.create_login.clicked.connect(lambda: self.login_create())
        self.submit_button.clicked.connect(lambda: self.submit())
        self.complete_button.clicked.connect(lambda: self.complete())
        self.logout_button.clicked.connect(lambda: self.logout())

        self.access_user()

    def clear(self) -> None:
        """Clears input from respective frame"""
        self.name_input.clear()
        self.age_ccount_number_input.clear()
        self.address_input.clear()
        self.pin_input.clear()
        self.set_balance_input.clear()
        self.welcome_label.clear()
        self.frame2.hide()
        self.frame3.hide()

    def enter(self) -> None:
        """ Shows frame1 and labeled inputs to create accounts/login"""
        if self.radioButton_account_create.isChecked():
            self.frame1.show()
            self.clear()
            self.age_account_number_label.setText('Age')
            self.address_label.show()
            self.address_input.show()
            self.set_balance_label.show()
            self.set_balance_input.show()
            self.create_login.setText('Create Account')
        elif self.radioButton_log_in.isChecked():
            self.frame1.show()
            self.clear()
            self.age_account_number_label.setText('Account Number')
            self.address_label.hide()
            self.address_input.hide()
            self.set_balance_label.hide()
            self.set_balance_input.hide()
            self.create_login.setText('Login')

    def access_user(self) -> None:
        """ Load user information from csvfile if it exists """
        try:
            with open(self.CSV_FILE, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    account_num = int(row['account_num'])
                    Logic.user_info[account_num] = {
                        'name': row['name'],
                        'age': int(row['pin']),
                        'address': row['address'],
                        'pin': int(row['pin']),
                        'balance': float(row['balance'])
                    }
        except FileNotFoundError:
            pass

    def save_user(self) -> None:
        """saves user information assuming it is not in csvfile """
        with open(self.CSV_FILE, 'w', newline='') as csvfile:
            fieldnames = ['account_num', 'name', 'age', 'address', 'pin', 'balance']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for account_num, user_info in Logic.user_info.items():
                writer.writerow({
                    'account_num': account_num,
                    'name': user_info['name'],
                    'age': user_info['age'],
                    'address': user_info['address'],
                    'pin': user_info['pin'],
                    'balance': user_info['balance']
                })

    def csv_update_bal(self, account_num: int, new_balance: float) -> None:
        """ Updates user balance in csvfile """
        Logic.user_info[account_num]['balance'] = new_balance
        self.save_user()

    def login_create(self) -> None:
        """displays frame 2
        Depending on the radio button selected events differ if create account radio button is selected
        it then validates information and transfers to csvfile
        if login checked radio button selected it validates info in csvfile and accesses account if it exists
        """
        if self.radioButton_account_create.isChecked():
            self.welcome_label.clear()
            self.name = self.name_input.text()
            self.age = self.age_ccount_number_input.text()
            self.address = self.address_input.text()
            self.pin = self.pin_input.text()
            self.set_balance = self.set_balance_input.text()
            try:
                self.age = int(self.age)
                self.pin = int(self.pin)
                self.balance = float(self.set_balance)
                if self.age >= 16:
                    self.acct_num = random.randint(10000, 99999)
                    self.clear()
                    self.welcome_label.setText(f"Welcome to G&M Banking. Your Account number is: {self.acct_num}.\n"
                                               f"Please save for future references. Happy Banking!")
                    Logic.user_info[self.acct_num] = {
                        'name': self.name,
                        'age': self.age,
                        'address': self.address,
                        'pin': self.pin,
                        'balance': float(self.balance)
                    }
                    self.save_user()
                    self.frame2.show()
                else:
                    self.clear()
                    self.welcome_label.setText('You are to young to open an account. Come back in a few years :)')
            except ValueError:
                self.clear()
                self.welcome_label.setText('Please enter valid information.')
        elif self.radioButton_log_in.isChecked():
            self.welcome_label.clear()
            self.name = self.name_input.text()
            self.acct_num = self.age_ccount_number_input.text()
            self.pin = self.pin_input.text()

            try:
                self.acct_num = int(self.acct_num)
                self.pin = int(self.pin)
                if self.cred_val():
                    self.clear()
                    self.welcome_label.setText(f"Welcome back {self.name}!")
                    self.frame2.show()

                else:
                    self.clear()
                    self.welcome_label.setText(f"Please enter valid information.")
            except ValueError:
                self.clear()
                self.welcome_label.setText(f"Invalid Account. Try again.")

    def cred_val(self) -> bool:
        """Confirms login credentials stored in csvfile in order to access bank information """
        if self.acct_num and int(self.acct_num) in Logic.user_info:
            user_info = Logic.user_info[int(self.acct_num)]
            return user_info['name'] == self.name and user_info['pin'] == self.pin
        else:
            return False

    def submit(self) -> None:
        """ displays frame3
        When transaction type is selected, relevant transaction options and user information is displayed
        """
        if self.radioButton_deposit.isChecked() or self.radioButton_withdraw.isChecked():
            self.frame3.show()
            self.trans_type_label.show()
            self.input_trans_amount.show()
            self.complete_button.show()
            if self.radioButton_deposit.isChecked():
                self.trans_type_label.setText('Deposit Amount')
            elif self.radioButton_withdraw.isChecked():
                self.trans_type_label.setText('Withdraw Amount')

            self.input_trans_amount.clear()
            self.available_balance_label.hide()
        elif self.radioButton_balance.isChecked():
            self.frame3.show()
            self.trans_type_label.hide()
            self.input_trans_amount.hide()
            self.complete_button.hide()
            self.available_balance_label.show()
            self.available_balance_label.setText(F"Available Balance: ${Logic.user_info[self.acct_num]['balance']}")

    def complete(self) -> None:
        """ Update, Withdraw, and Deposit transactions which are then processed and sent to csvfile"""
        if self.radioButton_deposit.isChecked() or self.radioButton_withdraw.isChecked():
            self.available_balance_label.clear()
            self.available_balance_label.hide()

            try:
                transaction_amount = float(self.input_trans_amount.text())
                if self.radioButton_deposit.isChecked():
                    Logic.user_info[self.acct_num]['balance'] += transaction_amount
                    self.csv_update_bal(self.acct_num, Logic.user_info[self.acct_num]['balance'])
                    self.available_balance_label.show()
                    self.available_balance_label.setText(f"Transaction Successful. \n"
                                                 f"Available balance: ${Logic.user_info[self.acct_num]['balance']:.2f}")
                elif self.radioButton_withdraw.isChecked():
                    if transaction_amount > Logic.user_info[self.acct_num]['balance']:
                        self.available_balance_label.show()
                        self.available_balance_label.setText('Withdrawal amount exceeds available balance')
                    else:
                        Logic.user_info[self.acct_num]['balance'] -= transaction_amount
                        self.csv_update_bal(self.acct_num, Logic.user_info[self.acct_num]['balance'])
                        self.available_balance_label.show()
                        self.available_balance_label.setText(f"Transaction Successful. \n"
                                                     f"Available balance: \n"
                                                     f"${Logic.user_info[self.acct_num]['balance']:.2f}")
                self.input_trans_amount.clear()
            except ValueError:
                self.available_balance_label.show()
                self.available_balance_label.setText('Please enter a valid numeric amount')

    def logout(self):
        """Closes the GUI """
        self.close()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    BankRegistration = QtWidgets.QMainWindow()
    ui = Ui_BankRegistration()
    ui.setupUi(BankRegistration)
    BankRegistration.show()
    sys.exit(app.exec())
