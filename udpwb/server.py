from socket import *
import time

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

for i in range(10):
    message = "Ping " + str(i + 1)

    start = time.perf_counter()

    clientSocket.sendto(message.encode(), (serverName, serverPort))

    try:
        reply, address = clientSocket.recvfrom(1024)

        end = time.perf_counter()
        rtt = (end - start) * 1000

        print("Reply received:", reply.decode())
        print("RTT:", round(rtt, 2), "ms")

    except timeout:
        print("Request timed out")

clientSocket.close()






