from socket import *
import random

serverPort = 12000

serverSocket = socket(AF_INET, SOCK_DGRAM)
serverSocket.bind(("", serverPort))

print("UDP Server is ready...")

while True:
    message, clientAddress = serverSocket.recvfrom(1024)

    if random.random() < 0.3:
        print("Packet dropped")
        continue

    reply = message.decode().upper()

    serverSocket.sendto(reply.encode(), clientAddress)