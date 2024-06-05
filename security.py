import datetime
import psutil
import hashlib
import os
import sys
import time

class Security:
    def __init__(self, protected_file_path):
        self.protected_file_path = protected_file_path
        self.password = None
        self.load_password()

    def set_password(self):
        while True:
            new_password = input("Enter a new password: ")
            confirm_password = input("Confirm the new password: ")
            if new_password == confirm_password:
                self.store_password(new_password)
                print("Password set successfully!")
                break
            else:
                print("Passwords do not match. Please try again.")

    def store_password(self, password):
        with open(self.protected_file_path, "w") as f:
            f.write(password)
        self.password = password  # Update the stored password

    def load_password(self):
        try:
            with open(self.protected_file_path, "r") as f:
                self.password = f.read()
        except FileNotFoundError:
            print(f"Password file '{self.protected_file_path}' not found. Setting a new password.")
            self.set_password()

    def check_password(self, entered_password):
        return entered_password == self.password

    def is_authorized_edit(self, process_name):
        authorized_apps = ["notepad.exe", "sublime_text.exe"]  # Replace with your list of authorized applications (process names)
        for app in authorized_apps:
            if app in process_name.lower():  # Check for case-insensitive match
                return True
        return False

    def protect_file(self, file_path):
        with open(file_path, 'r') as file:
            new_file_data = file.read()
            file.close()
        old_file_data = self.get_file_data(file_path)

        if old_file_data != new_file_data:
            if not self.is_authorized_edit(psutil.Process().name()):
                print(f" '{file_path}' was being edited by unauthorized application @{datetime.datetime.now()}")
                password = input("Enter password to allow edit or disable monitoring: ")
                if self.check_password(password):
                    print(f" '{file_path}' was edited by authorized application @{datetime.datetime.now()}")
                else:
                    print("Invalid password. File content reverted.")
                    self.restore_file_data(file_path, old_file_data)
            else:
                print(f" '{file_path}' was edited by authorized application @{datetime.datetime.now()}")

    def get_file_data(self, file_path):
        try:
            with open(file_path, 'r') as file:
                return file.read()
        except FileNotFoundError:
            return None

    def restore_file_data(self, file_path, data):
        with open(file_path, 'w') as file_write:
            file_write.write(data)
            file_write.close()

# # Example usage:
# if __name__ == "__main__":
#     print("")
#     print(" ▓ Prevedit")
#     print(" ▓ Make sure to put the required files in the 'filelist' folder.")
#     print(" ▓ If new files are stored in the 'filelist' folder after the program begins, it has to be restarted.")
#     print("")
#
#     # Checking if the required folder exists, creating it if necessary
#     if os.path.exists('filelist'):
#         pass
#     else:
#         try:
#             os.mkdir('filelist')
#         except PermissionError:
#             print(" The folder 'filelist' could not be created due to permission error. You can create it manually")
#             time.sleep(3)
#             sys.exit()
#
#     # Create a Security object, specifying the file to protect
#     security = Security("x7b4y1z6.dat")
#
#     # Now you can use the Security object's methods
#     security.protect_file("filelist/some_file.txt")  # Protect "some_file.txt" in the "filelist" folder