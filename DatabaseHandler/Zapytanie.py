class Zapytanie:
    """Klasa reprezentująca zapytanie do bazy danych.

    Zmienne
    ----------
    sql : str
        Kod sql do wykonania w ramach bazy danych
    query : List[Dict[str, Any]]
        Tabele wyników query powstałe na skutek wykonania kodu sql
    zmienoneRzędy : int
        Ilość zmienionych rzędów na skutek wykonania kodu sql
    wiadomości : str
        Wiadomości zwróceone z bazy dabych na skutek wykonania kodu sql
    error : str
        Błędy zwrócone na skutek wykonania kodu sql
    wykonane : bool
        Binarne określenie czy wykonano już zapytanie

    """

    def __init__(self, sql):
        """Inicjalizuje obiekt klasy Zapytanie.

        Argumenty
        ----------
        sql : str
            Kod sql do wykonania w ramach bazy danych

        """

        self.sql = sql

        self.query = None

        self.zmienoneRzędy = None
        self.wiadomości = None

        self.error = None

        self.wykonane = False

    def __str__(self):
        """Zwraca reprezentacje stringową zapytania.

            Argumenty
                ----------
                brak

            Zwraca
                -------
                str
                    wszystkie zmienne obiektu klasy (poza wykonnane) w kolejności zcastowane do stringa i rozdzielone ~~~

        """

        return f"{self.sql}~~~{self.query}~~~{self.zmienoneRzędy}~~~{self.wiadomości}~~~{self.error}"


