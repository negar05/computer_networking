from socket import *
import time

serverName = "127.0.0.1"
serverPort = 12000

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)

rtts = []
lostPackets = 0

for i in range(10):
    message = "Ping " + str(i + 1)

    start = time.perf_counter()

    clientSocket.sendto(message.encode(), (serverName, serverPort))

    try:
        reply, address = clientSocket.recvfrom(1024)

        end = time.perf_counter()
        rtt = (end - start) * 1000

        rtts.append(rtt)

        print("Reply received:", reply.decode())
        print("RTT:", round(rtt, 2), "ms")

    except timeout:
        lostPackets += 1
        print("Request timed out")

    time.sleep(1)

clientSocket.close()

print("\n--- Statistics ---")

if rtts:
    print("Minimum RTT:", round(min(rtts), 2), "ms")
    print("Maximum RTT:", round(max(rtts), 2), "ms")
    print("Average RTT:", round(sum(rtts) / len(rtts), 2), "ms")

print("Packet Loss:", lostPackets * 10, "%")