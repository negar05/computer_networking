from socket import *

proxyHost = "127.0.0.1"
proxyPort = 8888

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((proxyHost, proxyPort))

request = (
    "GET http://www.irna.ir/ HTTP/1.1\r\n"
    "Host: www.irna.ir\r\n"
    "Connection: close\r\n"
    "\r\n"
)

clientSocket.sendall(request.encode())

response = b""

while True:
    data = clientSocket.recv(4096)

    if not data:
        break

    response += data

print(response.decode("iso-8859-1"))

clientSocket.close()