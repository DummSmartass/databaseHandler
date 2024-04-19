class Zapytanie:
    def __init__(self, sql):
        self.sql = sql

        self.query = None
        self.error = None
        self.komunikaty = None

        self.wykonane = False

