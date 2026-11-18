from socket import *
proxyPort = 8888

serverHost = "127.0.0.1"
serverPort = 6789

proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

proxySocket.bind(("127.0.0.1", proxyPort))
proxySocket.listen(5)

print("Chat Proxy is ready...")

while True:

    clientSocket, clientAddress = proxySocket.accept()

    print("Client connected:", clientAddress)

    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.connect((serverHost, serverPort))

    while True:

        data = clientSocket.recv(1024)
        if not data:
            break

        print("From client:", data.decode())

        serverSocket.sendall(data)

        reply = serverSocket.recv(1024)

        if not reply:
            break

        print("From server:", reply.decode())

        clientSocket.sendall(reply)

    clientSocket.close()
    serverSocket.close()
