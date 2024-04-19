import socket
flag = False
"""
gui here
"""

"bramka sprawdzająca połączenie"
print("Connecting to server...", end="")
for x in range(6000, 6010):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(("127.0.0.1", x))
        s.settimeout(0.5)
        msg = s.recv(1024).decode()
        if msg == "connected":
            break
    except TimeoutError:
        print("#", end="")
    except ConnectionRefusedError:
        print("#", end="")
    s.close()

while True:
    msg = input("#>")
    s.send(msg.encode())
    if msg == "end":
        break

s.close()
