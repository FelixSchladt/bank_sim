import json
import time
import os
import hashlib
import aes
from tools import *
import transfer

def create(username, password):
    new_account = {
        "hash" : f"{get_account_hash(username, password)}",
        "username" : username,
        "password" : f"{get_salted_hash(password)}",
        "wallet"   : f"{get_salted_hash(username)[-32:]}",
        "balance"  : 0,
        "received_transfers" : [1],
        "sent_transfers" : [1],
        "time" : f"{get_time()}",
    }
    if not os.path.isdir("accounts"):
        os.mkdir("accounts")

    #with open(f"accounts{os.sep}{new_account['hash']}.json", "w") as write_file:
    #    json.dump(new_account, write_file, indent=4)

    aes.file_handler(new_account["hash"], password, True, new_account)
    del password, new_account

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

    def deposit(self, amount):
        self.__account["balance"] += amount
        self.__save_account()

    def withdraw(self, amount):
        self.__account["balance"] -= amount
        self.__save_account()

    def check_for_transfers(self):
        new = self.__transfer_obj.update()
        for transfer in new:
            self.deposit(transfer["amount"])
        print(self.__account)
        print(self.__account['received_transfers'])
        self.__account['received_transfers'].append(new)
        return len(new)

    def create_transfer(self, recipient, amount, usage):
        transfer = self.__transfer_obj.create(get_salted_hash(self.__username), recipient, amount, usage)
        self.withdraw(amount)
        self.__account["sent_transfers"].append(transfer)

    def get_username(self):
        return self.__account["username"]

    def get_wallet(self):
        return self.__account["wallet"]

    def get_balance(self):
        return self.__account["balance"]

    def get_received_transfers(self):
        return self.__account["received_transfers"]

    def get_sent_transfers(self):
        return self.__account["sent_transfers"]

    def get_time(self):
        return self.__account["time"]


#class accounts:
#    def __init__(self, account_id):

if __name__=="__main__":
    #create(input("username"), input("passwort"))
    create("test", "passwort")
    create("test2", "passwort")
    acc2 = account("test2", "passwort")
    acc = account("test", "passwort")
    print(acc.get_balance())
    acc.deposit(300)
    print(acc.get_balance())
    acc.create_transfer(acc2.get_wallet(), 100, "testing")
    acc2.check_for_transfers()
    print(acc2.get_balance())


