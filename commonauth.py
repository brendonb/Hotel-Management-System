# common.py
class User:
    def __init__(self, username):
        self.username = username
    # Common authentication parse to other classes ( Error with loop)
    def get_username(self):
        return self.username
