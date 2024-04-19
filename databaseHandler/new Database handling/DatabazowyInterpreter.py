import queue
import threading
import time

import pyodbc

class DatabazowyInterpreter:
    def __init__(self, bazaDanych):
        self.bazaDanych = bazaDanych
        self.wątekGłówny = self.my_thread = threading.Thread(target=self.wątekGłówny)
        self.kolejkaPoleceń = queue.Queue()
        self.logZapytań = queue.Queue()
        self.stop = False

    def wątekGłówny(self):
        try:
            połączenie = pyodbc.connect(self.bazaDanych)
            print("Połączono")
        except Exception as error:
            print(f"Błąd przy połączeniu {error}")

        try:
            while not self.stop:
                if not self.kolejkaPoleceń.empty():
                    zapytanie = self.kolejkaPoleceń.get()

                    if zapytanie.sql == 'EXIT':
                        return

                    try:
                        kursos = połączenie.cursor()
                        kursos.execute(zapytanie)
                        połączenie.commit()

                    except Exception as error:
                        zapytanie.errory = error

                    self.logZapytań.put(zapytanie)
                    zapytanie.wykonane=True

                else:
                    time.sleep(0.5)
        except Exception as error:
            print(f"Błąd przy przetwarazaniu zaptaniań {error}")

    def start(self):
        self.my_thread.start()

    def safeStop(self):
        self.dodajInstukcje(Zapytanie('EXIT'))

    def zabij(self):
        self.stop = True

    def dodajInstukcje(self, sql):
        self.kolejkaPoleceń.put(sql)


if __name__ == "__main__":


    interpreter1 = DatabazowyInterpreter('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=RPG;Trusted_Connection=yes;')
    interpreter1.start()
    request1 = Zapytanie("select * from Race")
    interpreter1.dodajInstukcje(request1)
    interpreter1.safeStop()

    while not request1.wykonane():
        time.sleep(0.5)
    print(request1.query)