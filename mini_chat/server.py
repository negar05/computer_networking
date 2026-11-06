from socket import *

serverPort = 6789

serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(("", serverPort))
serverSocket.listen(1)

print("Server is ready...")

connectionSocket, addr = serverSocket.accept()
print("Connected by:", addr)

while True:
    data = connectionSocket.recv(1024)

    if not data:
        break

    message = data.decode()
    print("Client:", message)

    if message == "exit":
        break

    reply = input("You: ")
    connectionSocket.sendall(reply.encode())

    if reply == "exit":
        break

connectionSocket.close()
serverSocket.close()