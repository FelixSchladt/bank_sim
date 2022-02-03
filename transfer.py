import json
import os
from tools import *
import aes

class transaction():
    def __init__(self, wallet):
        self.__wallet = wallet

        if not os.path.isdir("transactions"):
            os.mkdir("transactions")

    def update(self):
        files = os.listdir(f"transactions{os.sep}")
        transactions = []
        crypto_obj = aes.crypto_handler(self.__wallet)

        for file in files:
            with open(f"transactions{os.sep}{file}", "rb") as file_stream:
                try:
                    file_content = json.loads(crypto_obj.decrypt(file_stream.read()).decode())
                    if file_content["recipient"] == self.__wallet:
                        transactions.append(file_content)
                        self.__remove(f"transactions{os.sep}{file}")
                except Exception as ex:
                    pass
        return transactions

    def create(self, username_hash, target_wallet, amount, usage):
        crypto_obj = aes.crypto_handler(target_wallet)
        time = get_time()
        transaction = {
            "id"        : f"{get_salted_hash(target_wallet+time+username_hash)}",
            "submitter" : username_hash,
            "recipient" : target_wallet,
            "amount"    : amount,
            "usage"     : usage,
            "time"      : time,
        }

        with open(f"transactions{os.sep}{transaction['id']}", "wb") as transfer_file:
            transfer_file.write(crypto_obj.encrypt(json.dumps(transaction).encode()))

        return transaction

    def __remove(self, filename):
        os.remove(filename)
