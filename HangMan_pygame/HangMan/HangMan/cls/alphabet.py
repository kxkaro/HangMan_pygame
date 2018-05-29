import string


class Alphabet:

    def __init__(self):
        self.available = ""
        self.used = ""

    
    def reset(self):
        self.available = ""
        for c in string.ascii_uppercase: self.available = self.available + c + " "
        self.used = ""


    def update(self, c):
        self.available = self.available.replace(c.upper() + " ", "")
        self.used = self.used + c
