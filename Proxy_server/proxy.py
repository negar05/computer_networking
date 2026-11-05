
from socket import *

proxyPort = 8888

proxySocket = socket(AF_INET, SOCK_STREAM)
proxySocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
proxySocket.bind(("127.0.0.1", proxyPort))
proxySocket.listen(5)

print("Web Proxy is ready...")


while True:

    clientSocket, clientAddress = proxySocket.accept()

    try:
        
        requestData = b""

        while b"\r\n\r\n" not in requestData:
            chunk = clientSocket.recv(4096)

            if not chunk:
                break

            requestData += chunk

        if not requestData:
            clientSocket.close()
            continue

        requestText = requestData.decode("iso-8859-1")

        lines = requestText.split("\r\n")
        requestLine = lines[0].split()

        if len(requestLine) < 3:
            clientSocket.close()
            continue

        method, url, version = requestLine

        if method != "GET":
            clientSocket.sendall(
                b"HTTP/1.1 501 Not Implemented\r\n"
                b"Content-Length: 0\r\n"
                b"Connection: close\r\n\r\n"
            )
            clientSocket.close()
            continue

        if not url.startswith("http://"):
            clientSocket.sendall(
                b"HTTP/1.1 400 Bad Request\r\n"
                b"Content-Length: 0\r\n"
                b"Connection: close\r\n\r\n"
            )
            clientSocket.close()
            continue

        
        urlParts = url[7:].split("/", 1)

        hostAndPort = urlParts[0]

        if len(urlParts) == 2:
            path = "/" + urlParts[1]
        else:
            path = "/"

        if ":" in hostAndPort:
            serverHost, portText = hostAndPort.rsplit(":", 1)
            serverPort = int(portText)
        else:
            serverHost = hostAndPort
            serverPort = 80


        headers = []

        for line in lines[1:]:

            if not line:
                break

            if line.lower().startswith("proxy-connection:"):
                continue

            if line.lower().startswith("connection:"):
                continue

            headers.append(line)

        if not any(
            line.lower().startswith("host:")
            for line in headers
        ):
            headers.append(f"Host: {serverHost}")

        headers.append("Connection: close")


        newRequest = (
            f"{method} {path} {version}\r\n"
            + "\r\n".join(headers)
            + "\r\n\r\n"
        )


        originSocket = socket(AF_INET, SOCK_STREAM)
        originSocket.settimeout(10)

        originSocket.connect((serverHost, serverPort))


        originSocket.sendall(
            newRequest.encode("iso-8859-1")
        )


        while True:

            responseData = originSocket.recv(4096)

            if not responseData:
                break

            clientSocket.sendall(responseData)

        originSocket.close()
        clientSocket.close()

    except Exception as error:

        print("Proxy error:", error)

        try:
            clientSocket.close()
        except OSError:
            pass
