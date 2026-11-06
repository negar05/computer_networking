from socket import *

serverName = "127.0.0.1"
serverPort = 6789

clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))

while True:
    message = input("You: ")
    clientSocket.sendall(message.encode())

    if message == "exit":
        break

    data = clientSocket.recv(1024)

    if not data:
        break

    reply = data.decode()
    print("Server:", reply)

    if reply == "exit":
        break

clientSocket.close()