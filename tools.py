import time
import hashlib

def get_hash(content):
    return hashlib.sha512(content.encode()).hexdigest()

def get_account_hash(username, password):
    salt = f"{username[int(len(username)/3)]}salt{password[int(len(password)/2)]}"
    return get_hash(f"{username}{salt}{password}")

def get_salted_hash(username):
    salt = f"{username[int(len(username)/3)]}salty]"
    return get_hash(f"{username}{salt}")

def get_time():
    return time.strftime("%m.%d.%Y %H:%M:%S", time.localtime())
