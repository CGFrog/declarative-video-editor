class Token():

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def toString(self):
        return f"({self.key}, {self.value})"