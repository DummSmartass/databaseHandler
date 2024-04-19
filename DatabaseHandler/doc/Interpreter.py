import time

from DatabazowyLink import DatabazowyLink
from Zapytanie import Zapytanie


class Interpreter:
    """Klasa służąca do przryjmowania komend i interpretowania ich

        Zmienne
        ----------
        linkDoBazy : DatabazowyLink
            link do bazy danych przez który można wchodzić z nią w interakcje
        switche : [Dict[str, Function]
            switch dopasowujący nazwy funkcji do funkcjii

    """

    def GETALL(self, instrukcja):
        """Zwraca w formie zapytania wynik pobrania nazw wszystkich tabel w bierzącej bazie danych

            Argumenty
            ----------
                instrukcja : str
                    komenda bez nagłówka

            Zwraca
                -------
                Zapytanie
                    zrealizowane zapytanie zawierające w query nazwy wszystkich tabel w obecnej bazie dnaych
        """

        zapytanie = Zapytanie("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE = 'BASE TABLE'")
        self.linkDoBazy.dodajInstukcje(zapytanie)
        while not zapytanie.wykonane:
            time.sleep(0.5)
        return zapytanie

    def GETCOLUMNS(self, instrukcja):
        """Zwraca zapytanie zawierające liste nazw wszystkich kolumn w tabeli o podanej nazwie w bierzącej bazie danych

            Argumenty
            ----------
                instrukcja : str
                    komenda bez nagłówka

            Zwraca
                -------
                Zapytanie
                    zrealizowane zapytanie zawierające w query nazw kolumn podanej tabeli
        """

        zapytanie = Zapytanie(f"SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = '{instrukcja.split(' ',1)[1]}'")
        self.linkDoBazy.dodajInstukcje(zapytanie)
        while not zapytanie.wykonane:
            time.sleep(0.5)
        return zapytanie

    def GETCONTENT(self, instrukcja):
        """Zwraca zawartość podanej tabeli.

            Argumenty
            ----------
                instrukcja : str
                    komenda bez nagłówka

            Zwraca
                -------
                Zapytanie
                    zrealizowane zapytanie zawierające w query zawarartość tabeli o podnaje nazwie
        """

        zapytanie = Zapytanie(f"SELECT * from {instrukcja.split(' ',1)[1]}")
        self.linkDoBazy.dodajInstukcje(zapytanie)
        while not zapytanie.wykonane:
            time.sleep(0.5)
        return zapytanie

    def DIRECT(self, instrukcja):
        """Zwraca wynik wysłania instrukcji do bazy danych

            Argumenty
            ----------
                instrukcja : str
                    komenda bez nagłówka

            Zwraca
                -------
                Zapytanie
                    zrealizowane zapytanie zawierające z sqlem takim jak podana instrukcja
        """

        zapytanie = Zapytanie(instrukcja.split(' ',1)[1])
        self.linkDoBazy.dodajInstukcje(zapytanie)
        while not zapytanie.wykonane:
            time.sleep(0.5)
        return zapytanie


    def default(self,instrukcja):
        """Zwraca błąd nieznanej komendy

            Argumenty
            ----------
                instrukcja : str
                    komenda bez nagłówka

            Zwraca
                -------
                Zapytanie
                    zapytanie z błędem indykującym nie wykrycie komendy
        """

        zapytanie = Zapytanie(instrukcja)
        zapytanie.error = "NOT FOUND"
        return  zapytanie


    def __init__(self):
        """Inicjalizuje obiekt klasy Interpreter.

            Argumenty0
            ----------
                brak
        """

        self.linkDoBazy = None
        self.switche = {
            "GETALL":self.GETALL,
            "GETCOLUMNS": self.GETCOLUMNS,
            "GETCONTENT": self.GETCONTENT,
            "DIRECT": self.DIRECT
        }


    def interpretuj(self,instrukcja):
        """interpretuje podaną instrukcje

            Argumenty
                ----------
                instrukcja : str
                    komenda do rozpoznania i wykonania
        """

        return self.switche.get(instrukcja.split(" ")[0], self.default)(instrukcja)

    def utwórzLink(self,connectionString):
        """tworzy połączenie z bazą danych tworząc link do bazy danej do której prowadzi connectionString

            Argumenty
                ----------
                connectionString : str
                    connectionString do łączenia się z bazą danych
        """

        databazowyLink = DatabazowyLink(connectionString)
        databazowyLink.start()

        self.linkDoBazy = databazowyLink



if __name__ == "__main__":
    interpreter1 = Interpreter()
    interpreter1.utwórzLink('DRIVER={SQL Server};SERVER=localhost\\SQLEXPRESS;DATABASE=RPG;Trusted_Connection=yes;')
    print(interpreter1.interpretuj("DIRECT select * from Race"))
