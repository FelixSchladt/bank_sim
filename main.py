#!/usr/bin/python
#import curses #only for *nix systems
#reprint seems to be cross platform https://github.com/Yinzo/reprint/blob/master/reprint/reprint.py
import sys
import signal
import accounts
import re
import getpass

class c:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def signal_handler(sig, frame):
    print("\n\nExiting application...")
    sys.exit(0)


class terminal():
    def __init__(self):
        self.welcome()

    def welcome(self):
        usr_input = input(f"\n{c.UNDERLINE}{c.BOLD}Welcome to bank simulator{c.ENDC}\n\n1. Login\n2. Create account\n3. Exit\n\n: ")
        if usr_input == "1":
            self.clear()
            self.login(0)
        elif usr_input == "2":
            self.clear()
            self.create()
        elif usr_input == "3":
            sys.exit(0)
        else:
            print("Invalid input")
            self.welcome()

    def clear(self):
        print("\n------------------------------------------------------------\n")

    def login(self, attempts):
        print (f"{c.BOLD}{c.UNDERLINE}Login\n{c.ENDC}")
        if attempts > 2:
            self.welcome()
        try:
            self.account = accounts.account(input("Username: "), getpass.getpass())
        except Exception:
            print(f"Invalid credentials: {3-attempts} attempts left")
            self.login(attempts+1)
        self.clear()
        self.account_main_menu()

    def account_main_menu(self):
        usr = input(f"{c.BOLD}{c.UNDERLINE}Main Menu: {self.account.get_username()}{c.ENDC}\n{c.OKGREEN}Current balance = {self.account.get_balance()}{c.ENDC}\n\n1. Cash deposit\n2. Cash withdraw\n3. Transfer to bank account\n4. Show transactions\n5. Show wallet id\n6. Logout\n\n: ")

        if usr == "1":
            self.clear()
            self.deposit()
        elif usr == "2":
            self.clear()
            self.withdraw()
        elif usr == "3":
            self.clear()
            self.transfer(0)
        elif usr == "4":
            self.clear()
            self.show_transfers()
        elif usr == "5":
            self.clear()
            self.show_wallet()
        elif usr == "6":
            self.clear()
            self.welcome()
        else:
            print(f"{c.WARNING}invalid input{c.ENDC}\n")
            self.account.get_transfers()
            self.clear()
            self.account_main_menu()

    def deposit(self):
        usr = input(f"{c.BOLD}{c.UNDERLINE}Deposit{c.ENDC}\n{c.OKGREEN}Balance = {self.account.get_balance()}{c.ENDC}\nType amount or hit enter to leave\n\n:")
        if usr.isnumeric():
            usr = float(usr)
            try:
                self.account.deposit(float(usr))
                print("Success")
            except Exception:
                print("Invalid amount")
            finally:
                self.clear()
                self.account_main_menu()
        else:
            self.clear()
            self.account_main_menu()

    def withdraw(self):
        usr = input(f"{c.BOLD}{c.UNDERLINE}Withdraw{c.ENDC}\n{c.OKGREEN}Balance = {self.account.get_balance()}{c.ENDC}\n\nType amount or hit enter to leave\n\n:")
        if usr.isnumeric():
            usr = float(usr)
            try:
                self.account.withdraw(float(usr))
                print("Success")
            except Exception:
                print("Insufficient funds or invalid amount")
            finally:
                self.clear()
                self.account_main_menu()
        else:
            self.clear()
            self.account_main_menu()

    def transfer(self, step):
        def check_exit(usr):
            if usr == "":
                self.clear()
                self.account_main_menu()

        if step == 0:
            print(f"{c.BOLD}{c.UNDERLINE}Transfer money{c.ENDC}\n{c.OKGREEN}Balance = {self.account.get_balance()}{c.ENDC}\n'ENTER' to leave\n")
            self.__wallet = input("Recipient Wallet: ")
            check_exit(self.__wallet)

            if len(self.__wallet) != 32:
                print(f"\n{c.FAIL}invalid wallet{c.ENDC}")
                self.transfer(0)
            self.transfer(1)
        elif step == 1:
            self.__amount = input("Amount: ")
            check_exit(str(self.__amount))
            if not self.__amount.isnumeric():
                print("Invalid input\n")
                self.transfer(1)
            self.__amount = int(self.__amount)
            if self.__amount > self.account.get_balance() or self.__amount < 0:
                print("Invalid amount")
                self.transfer(1)
            self.transfer(2)
        elif step == 2:
            self.__reason = input("Notice: ")
            check_exit(self.__reason)
            try:
                self.account.create_transfer(self.__wallet, self.__amount, self.__reason)
                print(f"{c.OKGREEN}Success{c.ENDC}")
            except Exception as ex:
                print(f"{c.FAIL}Failure{c.ENDC}", ex)
            finally:
                self.clear()
                self.account_main_menu()

    def show_transfers(self):
        print(f"{c.BOLD}{c.UNDERLINE}Most recent transactions{c.ENDC}\n{c.OKGREEN}Balance = {self.account.get_balance()}{c.ENDC}\n'ENTER' to leave\n-------")
        transactions = self.account.get_transfers()
        for transaction in transactions:
            print(transaction)
            print(f"ID:      {transaction['id']}")
            print(f"From:    {transaction['submitter']}")
            print(f"To:      {transaction['recipient']}")
            if transaction["amount"] > 0:
                print(f"Amount: {c.OKGREEN}+{transaction['amount']}{c.ENDC}")
            else:
                print(f"Amount:  {c.FAIL}{transaction['amount']}{c.ENDC}")
            print(f"Message: {transaction['usage']}")
            print(f"Date:    {transaction['time']}")
            print("------")

        input()
        self.clear()
        self.account_main_menu()

    def create(self, username=None):
        if not username:
            username = input(f"{c.BOLD}{c.UNDERLINE}Create new account{c.ENDC}\n\nUsername: ")
        psd = getpass.getpass()
        if psd != getpass.getpass("Repeat: "):
            print(f"\n{c.FAIL}Passwords do not match{c.ENDC}\nPlease retry:")
            self.create(username)
        if not re.fullmatch(r"[A-Za-z0-9@#!$*+&?=%]{8,}", psd):
            print(f"\n{c.FAIL}Password contains non supported character(s){c.ENDC}\nPlease retry:")

        try:
            accounts.create(username, psd)
            self.account = accounts.account(username, psd)
        except Exception:
            print(f"{c.FAIL}Process failed, try again and choose different username{c.ENDC}")
            self.clear()
            self.welcome()
        self.clear()
        self.account_main_menu()

    def show_wallet(self):
        input(f"{c.BOLD}{c.UNDERLINE}Your Wallet:{c.ENDC}\n\n'ENTER' to leave\n\n{self.account.get_wallet()}\n\n: ")
        self.clear()
        self.account_main_menu()



if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    terminal()
