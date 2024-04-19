import socket
import threading

from DatabazowyLink import DatabazowyLink
from Interpreter import Interpreter
from Zapytanie import Zapytanie

#linkiDoBazy = {}#MOJE  NIE RUSZAĆ

# MJUSIAŁEM TO TU PRZENIEŚĆ BO TO NIE KLASA I NIE MAM TU DOSTĘPU Z ZEWNĄTRZ
# łączenie z bazą danych NIE DOTYKAĆ


def connectTo(interpreter,instrukcja,linkiDoBazy):
    """Łączy interpreter z bazą danych posiłkując się lista aktywnych linków do bazy (uniknięcie jednoczesnego niekontrolowanego dostępu)

        Argumenty
            ----------
            interpreter : Interpreter
                Interpreter który trzeba połaczyć z bazą danych
            instrukcja : str
                Instrukcja zawierająca connection string do bazy danych
            linkiDoBazy : tuple[DatabazwyLink]

        Zwraca
            -------
            Zapytanie
                zapytanie łączące z bazą danych z wynikiem połączenia

    """

    interpreter.linkDoBazy = None

    zapytanie = Zapytanie(instrukcja.split(" ",1)[1])

    if zapytanie.sql in linkiDoBazy:
        interpreter.linkDoBazy = linkiDoBazy[instrukcja.split(" ", 1)[1]]
        zapytanie.wiadomości = "Ok"
    else:
        try:
            interpreter.utwórzLink(zapytanie.sql)
            linkiDoBazy[zapytanie.sql]=interpreter.linkDoBazy
            zapytanie.wiadomości = "Ok"
        except Exception as error:
            zapytanie.wiadomości = "nie Ok"
            zapytanie.error = error

    zapytanie.wykonane = True

    return zapytanie


def connection(port,linkiDoBazy):


    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("127.0.0.1", port))
    s.listen(0)
    c, addr = s.accept()
    print("[", port, "]==>", "connection received form", addr)
    c.send("connected".encode())

    interpreter = Interpreter() # MOJE  NIE RUSZAĆ

    while True:
        try:
            msg = c.recv(1024).decode()

            # TU SIĘ MOJE ZACZYNA
            print("=====interpretuje=====")

            if msg.split(" ")[0] == "CONNECT":
                print(connectTo(interpreter,msg,linkiDoBazy)) # zwracaj do klienta
            else:
                if interpreter.linkDoBazy == None:
                    zapytanie = Zapytanie(msg)
                    zapytanie.error = "nie jesteś połączony do bazy danych"
                    print(zapytanie)#  zwracaj do klienta
                else:
                    print(interpreter.interpretuj(msg))#zwracaj do klienta
            #TU SIĘ MOJE KOŃCZY


        except ConnectionResetError:
            print("Remote host killed connection...")
            break
        if msg == "end" or msg == "":
            print("[", port, "]==>", "Closing connection...")
            break
        # elif msg == "function1":
        #     print("Example function nr 1")
        # elif msg == "function2":
        #     print("Example function nr 2")
        # print("[", port, "]->", msg)
    c.close()
    s.close()
    connection(port)


linkiDoBazy = {}#MOJE NIE RUSZAĆ
print("--------------------------------------------------------")
print("|  Server for handling pro gamer connections :):):):)  |")
print("|                   Version 0.0.1                      |")
print("--------------------------------------------------------")
threads = []
flag = False
start = 6000
max_ports_number = int(input("Give max number of ports to open: "))
for x in range(start, (start+max_ports_number)):
    thread = threading.Thread(target=connection, args=(x,linkiDoBazy))
    threads.append(thread)
    thread.start()

for z in threads:
    z.join()

