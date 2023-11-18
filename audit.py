# common.py

#from login import globally_logged_class
class Audit:
    def __init__(self, username):
        self.username = username
    # Global variable to parse user to be audited on finance
    def get_audited_user(self):
        print("username from audit:", self.username)
        return self.username


