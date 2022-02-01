import json
import os
from tools import *

class transaction():
    def __init__(self, wallet):
        self.__wallet = wallet

        if not os.path.isdir("transactions"):
            os.mkdir("transactions")

    def update(self):
        files = os.listdir(f"transactions{os.sep}")
        transactions = []
        for file in files:
            with open(f"transactions{os.sep}{file}", "r") as file_stream:
                file_content = json.load(file_stream)
                if file_content["recipient"] == self.__wallet:
                    transactions.append(file_content)
                    self.__remove(f"transactions{os.sep}{file}")
        return transactions

    def create(self, username_hash, target_wallet, amount, usage):
        time = get_time()
        transaction = {
            "id"        : f"{get_salted_hash(target_wallet+time+username_hash)}",
            "submitter" : username_hash,
            "recipient" : target_wallet,
            "amount"    : amount,
            "usage"     : usage,
            "time"      : time,
        }

        with open(f"transactions{os.sep}{transaction['id']}", "w") as transfer_file:
            json.dump(transaction, transfer_file)

        return transaction

    def __remove(self, filename):
        os.remove(filename)
