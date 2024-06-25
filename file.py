# password_manager.py

import getpass
import hashlib
import os
import pickle

class PasswordManager:
    def __init__(self, master_password):
        self.master_password = master_password
        self.passwords = {}

    def add_password(self, service, password):
        self.passwords[service] = password

    def get_password(self, service):
        return self.passwords.get(service)

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.passwords, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.passwords = pickle.load(f)

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def main():
    master_password = getpass.getpass("Enter master password: ")
    hashed_master_password = hash_password(master_password)

    if os.path.exists("passwords.dat"):
        with open("passwords.dat", 'rb') as f:
            stored_hash = pickle.load(f)
            if stored_hash!= hashed_master_password:
                print("Incorrect master password")
                return
    else:
        with open("passwords.dat", 'wb') as f:
            pickle.dump(hashed_master_password, f)

    pm = PasswordManager(master_password)

    while True:
        print("1. Add password")
        print("2. Get password")
        print("3. Save and exit")
        choice = input("Choose an option: ")

        if choice == "1":
            service = input("Enter service: ")
            password = getpass.getpass("Enter password: ")
            pm.add_password(service, password)
        elif choice == "2":
            service = input("Enter service: ")
            password = pm.get_password(service)
            if password:
                print("Password:", password)
            else:
                print("No password found for", service)
        elif choice == "3":
            pm.save("passwords.dat")
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()