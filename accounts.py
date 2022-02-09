import json
import time
import os
import hashlib
import aes
from tools import *
import transfer

def create(username, password):
    transaction = get_transaction("Welcome", "Your Bank", 25, "Welcome present")
    new_account = {
        "hash" : f"{get_account_hash(username, password)}",
        "username" : username,
        "password" : f"{get_salted_hash(password)}",
        "wallet"   : f"{get_salted_hash(username)[-32:]}",
        "balance"  : 25,
        "transfers" : [transaction],
        "time" : f"{get_time()}",
    }
    if not os.path.isdir("accounts"):
        os.mkdir("accounts")

    if os.path.isfile(f"accounts{os.sep}{new_account['hash']}{aes.POSTFIX}"):
        print("This username ist taken...")

    aes.file_handler(new_account["hash"], password, True, new_account)

class account():
    def __init__(self, username, password):
        self.__username = username
        self.__password = password
        self.__account_hash = get_account_hash(username, password)

        self.__unlock_account()
        self.__transfer_obj = transfer.transaction(self.__account["wallet"])
        self.check_for_transfers()

    def __unlock_account(self):
        self.__account_obj = aes.file_handler(self.__account_hash, self.__password)
        self.__account = self.__account_obj.decrypt()

    def __save_account(self):
        self.__account_obj.encrypt(self.__account)

    def __deposit(self, amount):
        self.__account["balance"] += amount
        self.__save_account()

    def __withdraw(self, amount):
        self.__account["balance"] -= amount
        self.__save_account()

    def withdraw(self, amount):
        if amount < 0:
            raise Exception("negative_withdraw")
        transaction = get_transaction(self.__account["username"],
                                      self.__account["wallet"],
                                      -1*amount,
                                      "Cash withdraw")
        self.__account["transfers"].append(transaction)
        self.__withdraw(amount)

    def deposit(self, amount):
        if amount < 0:
            raise Exception("negative_deposit")
        transaction = get_transaction(self.__account["username"],
                                      self.__account["wallet"],
                                      amount,
                                      "Cash deposit")
        self.__account["transfers"].append(transaction)
        self.__deposit(amount)

    def check_for_transfers(self):
        new = self.__transfer_obj.update()
        for transfer in new:
            self.__deposit(transfer["amount"])
        if new:
            for transaction in new:
                self.__account['transfers'].append(transaction)
        return len(new)

    def create_transfer(self, recipient, amount, usage):
        if amount < 0:
            raise Exception("negative_amount")
        transfer = self.__transfer_obj.create(get_salted_hash(self.__username), recipient, amount, usage)
        self.__withdraw(amount)
        self.__account["transfers"].append(transfer)
        self.__save_account()

    def get_username(self):
        return self.__account["username"]

    def get_wallet(self):
        return self.__account["wallet"]

    def get_balance(self):
        return self.__account["balance"]

    def get_transfers(self):
        self.check_for_transfers()
        return self.__account["transfers"]

    def get_time(self):
        return self.__account["time"]


if __name__=="__main__":
    create("test", "passwort")
    create("test2", "passwort")
    acc2 = account("test2", "passwort")
    acc = account("test", "passwort")
    acc.deposit(300)
    print("Acc1: ", acc.get_balance())
    print("Acc2: ", acc2.get_balance())
    print("Acc1: making transfer to Acc2: 100")
    acc.create_transfer(acc2.get_wallet(), 100, "testing")
    acc2.check_for_transfers()
    print("Acc1: ", acc.get_balance())
    print("Acc2: ", acc2.get_balance())
    print("Transactions Acc: ", acc2.get_transfers())


