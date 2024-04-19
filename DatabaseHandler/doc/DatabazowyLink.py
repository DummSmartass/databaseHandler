import queue
import threading
import time

import pyodbc

from Zapytanie import Zapytanie


class DatabazowyLink:
    """Klasa reprezentująca zapytanie do bazy danych.

        Zmienne
        ----------
        bazaDanych : str
            connection string do bazy danych
        bazaDanych : str
            Connection string do bazy danych
        wątekGłówny : threat
            Wątek w którym przetwarzane są zapytania
        kolejka poleceń : queue
            Kolejka trzymające zapytania do wykonania
        blokada : Lock
            Zamek służący do kontroli przyjmowania nowych zapytań
        stop : bool
            Indykator zatrzymania działania zmieniany na true kiedy aplikacja ma zostać zakończona

    """

    def __init__(self, bazaDanych):
        """Inicjalizuje obiekt klasy Zapytanie.

            Argumenty
                ----------
                bazaDanych : str
                Connection string do połączenia z bazą danych

        """

        self.bazaDanych = bazaDanych
        self.wątekGłówny = self.my_thread = threading.Thread(target=self.wątekGłówny)
        self.kolejkaPoleceń = queue.Queue()
        self.blokada = threading.Lock()
        self.stop = False


    def wątekGłówny(self):
        """ przechodzi po kolejce zapytań i wykonuje je

            Argumenty
            ----------
                brak

        """

        połączenie = None

        try:
            połączenie = pyodbc.connect(self.bazaDanych)
            print("Połączono")
        except Exception as error:
            print(f"Błąd przy połączeniu {error}")

        try:
            while not self.stop:
                if not self.kolejkaPoleceń.empty():
                    zapytanie = self.kolejkaPoleceń.get()
                    print(zapytanie.sql)

                    if zapytanie.sql == 'EXIT':
                        return

                    try:
                        kursos = połączenie.cursor()
                        kursos.execute(zapytanie.sql)

                        try:
                            zapytanie.wiadomości = kursos.messages
                        except Exception as error:
                            a=1

                        try:
                            zapytanie.zmienoneRzędy = kursos.rowcount
                        except Exception as error:
                            a=1

                        try:
                            zapytanie.query = kursos.fetchall()
                        except Exception as error:
                            a=1

                        połączenie.commit()


                    except Exception as error:
                        zapytanie.error = error

                    zapytanie.wykonane=True

                else:
                    time.sleep(0.5)
        except Exception as error:
            print(f"Błąd przy przetwarazaniu zaptaniań {error}")

    def start(self):
        """Rozpoczyna działanie wątku głównego i przetwarazabnie zapytań.

            Argumenty
                ----------
                brak

        """
        self.my_thread.start()

    def safeStop(self):
        """Rozpoczyna bezpieczne zatrzymanie połączenia dodając na koniec koleji komende kończącą.

            Argumenty
                ----------
                brak

        """
        self.dodajInstukcje(Zapytanie('EXIT'))

    def zabij(self):
        """Zatrzymuje działanie Linkudatabazowego natychmiasotowo niezależnie od stanu kolejki

            Argumenty
                ----------
                brak

        """
        self.stop = True

    def dodajInstukcje(self, sql):
        """ bezpiecznie dodaje wiadmość do kolejki zapytań

            Argumenty
                ----------
                sql : str
                    kod sql do przekazania do kolejki

        """
        self.blokada.acquire()

        try:
            self.kolejkaPoleceń.put(sql)
        finally:
            self.blokada.release()


# if __name__ == "__main__":
#     interpreter1 = DatabazowyLink('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=RPG;Trusted_Connection=yes;')
#     interpreter1.start()
#     request1 = Zapytanie("select * from Race")
#     interpreter1.dodajInstukcje(request1)
#
#     while not request1.wykonane:
#         time.sleep(0.5)
#     print("query")
#     print(request1.query)
#     print("error")
#     print(request1.error)
#     print("rzędy")
#     print(request1.zmienoneRzędy)
#     print("wiadomości")
#     print(request1.wiadomości)
#
#     time.sleep(100)
#
#     request1 = Zapytanie("select * from Race")
#     interpreter1.dodajInstukcje(request1)
#     while not request1.wykonane:
#         time.sleep(0.5)
#     print("query")
#     print(request1.query)
#     print("error")
#     print(request1.error)
#     print("rzędy")
#     print(request1.zmienoneRzędy)
#     print("wiadomości")
#     print(request1.wiadomości)
#
#     interpreter1.safeStop()